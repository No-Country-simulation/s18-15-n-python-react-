from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from bson import ObjectId
from datetime import datetime
import pymongo
from config import MONGO_DETAILS
from models import UserCreate

# Conectar a MongoDB
client = pymongo.MongoClient(MONGO_DETAILS)
db = client["Taskmanager"]
users_collection = db['users']

# Inicializar el contexto de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Crear el router para las rutas de autenticación
router = APIRouter()

def get_password_hash(password: str) -> str:
    """Devuelve el hash de una contraseña."""
    return pwd_context.hash(password)

@router.post("/register", status_code=status.HTTP_201_CREATED, tags=["users"])
async def register_user(user: UserCreate): 
    """Registra un nuevo usuario con correo y contraseña."""

    # Verificar si el correo ya está registrado
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado."
        )

    # Encriptar la contraseña antes de guardarla
    hashed_password = get_password_hash(user.password)

    # Crear el nuevo usuario usando el modelo UserCreate
    new_user = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "hashed_password": hashed_password,
        "auth_provider": "local",  
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "profile_img": user.profile_img,  
        "google_id": None,  
        "email_verified": False,
        "tasks": []
    }

    # Insertar el nuevo usuario en la base de datos
    result = users_collection.insert_one(new_user)

    if result.inserted_id:
        return {
            "message": "Usuario registrado exitosamente.",
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar al usuario."
        )
