from fastapi import APIRouter, Request, HTTPException
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.config import Config
from fastapi.responses import RedirectResponse
from config import CLIENT_ID, CLIENT_SECRET
from jose import jwt
import httpx

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
