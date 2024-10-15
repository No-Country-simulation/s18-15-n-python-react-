from fastapi import APIRouter, Request, HTTPException
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.config import Config
from fastapi.responses import RedirectResponse
from config import CLIENT_ID, CLIENT_SECRET
from jose import jwt
from bson import ObjectId
from datetime import datetime
import httpx
import pymongo  

from config import MONGO_DETAILS

# Conectar a MongoDB
client = pymongo.MongoClient(MONGO_DETAILS)  
db = client["Taskmanager"]
users_collection = db['users']

config = Config('.env')

# Registrar cliente de OAuth con Google
oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={'scope': 'openid email profile'}
)

router = APIRouter()

@router.get("/login")
async def login(request: Request):
    """Redirige al usuario para autenticarse con Google."""
    redirect_uri = 'http://localhost:8000/auth/callback'
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_callback(request: Request):
    """Callback después de que el usuario se autentica con Google."""
    try:
        token = await oauth.google.authorize_access_token(request)

        if 'id_token' not in token:
            raise HTTPException(status_code=400, detail="No se recibió id_token.")

        # Decodificar el ID token proporcionando el access_token
        user_info = await parse_id_token(token['id_token'], token['access_token'])

        # **Lógica para registrar el usuario en MongoDB**
        email = user_info.get('email')
        first_name = user_info.get('given_name')
        last_name = user_info.get('family_name', '')
        profile_img = user_info.get('picture')
        google_id = user_info.get('sub')
        email_verified = user_info.get('email_verified', False)
        last_login = datetime.utcnow()

        # Verificar si el usuario ya existe en la base de datos
        existing_user = users_collection.find_one({"email": email})

        if existing_user:
            # Si el usuario ya existe, actualiza la fecha de último inicio de sesión
            users_collection.update_one(
                {"_id": existing_user["_id"]},
                {"$set": {"last_login": last_login}}
            )
        else:
            # Si el usuario no existe, crear un nuevo registro
            new_user = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "profile_img": profile_img,
                "google_id": google_id,
                "email_verified": email_verified,
                "auth_provider": "google",
                "last_login": last_login,
                "created_at": last_login,
                "updated_at": last_login,
                "tasks": []  # Inicializa la lista de tareas vacía
            }
            users_collection.insert_one(new_user)

        # Retornar mensaje de bienvenida
        return {"message": f"Welcome user: {user_info.get('given_name', 'Usuario')}, Email: {user_info.get('email', 'No email')}"}

    except OAuthError as error:
        print("OAuth error:", error)
        raise HTTPException(status_code=400, detail=str(error))


async def parse_id_token(id_token: str, access_token: str):
    """Verificar y decodificar el ID token."""
    try:
        jwks_url = "https://www.googleapis.com/oauth2/v3/certs"
        
        async with httpx.AsyncClient() as client:
            jwks = await client.get(jwks_url)
            jwks = jwks.json()

        # Decodificar el ID token proporcionando el access_token para validar at_hash
        payload = jwt.decode(id_token, jwks, algorithms=["RS256"], options={"verify_aud": False}, access_token=access_token)

        return payload  # retorno del payload que contiene información del usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al decodificar el ID token: " + str(e))


@router.get("/logout")
async def logout(request: Request):
    """Cierra la sesión del usuario."""
    request.session.clear()
    return RedirectResponse(url="/")
