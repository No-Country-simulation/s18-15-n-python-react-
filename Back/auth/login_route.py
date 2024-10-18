from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import pymongo
import jwt  
from config import MONGO_DETAILS, SECRET_KEY, ALGORITHM
from bson import ObjectId
from datetime import datetime, timedelta, timezone

# Conectar a MongoDB
client = pymongo.MongoClient(MONGO_DETAILS)
db = client["Taskmanager"]
users_collection = db['users']

# Inicializar el contexto de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Definir el esquema de entrada para el inicio de sesión
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Crear el router para las rutas de autenticación
router = APIRouter()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña proporcionada coincide con la almacenada."""
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(user_id: str) -> str:
    """Genera un token JWT usando el ID del usuario."""
    payload = {
        "sub": str(user_id),  # Usar el ID del usuario
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)  # Expira en 1 hora
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm= ALGORITHM)
    return token

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user: UserLogin):
    """Inicia sesión con correo y contraseña."""
    
    # Buscar el usuario en la base de datos
    existing_user = users_collection.find_one({"email": user.email})
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos."
        )

    # Verificar la contraseña
    if not verify_password(user.password, existing_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos."
        )

    # Generar un JWT usando el ID del usuario
    token = create_jwt_token(existing_user["_id"])
   

    return {"message": "Inicio de sesión exitoso", "token": token}
