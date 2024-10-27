from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from config import MONGO_DETAILS
from dependencies import get_user_id
from models import UserUpdate
from pymongo import MongoClient
from passlib.context import CryptContext

# Configurar el contexto de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Conectar a la base de datos MongoDB
client = MongoClient(MONGO_DETAILS)
db = client["Taskmanager"]
users_collection = db['users']

# Crear el router para las rutas de usuarios
router = APIRouter()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#Ruta que permite cambiar  el nombre, apellido e imagen de perfil de un usuario, 

@router.put('/update', tags=["users"], response_model=dict)
async def update_user(user_data: UserUpdate, user_id: str = Depends(get_user_id)):
    # Verifica si el usuario existe
    existing_user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado o acceso no autorizado")
    
    # Excluye campos no enviados en la solicitud y actualiza solo los establecidos
    updated_fields = user_data.model_dump(exclude_unset=True)

    # Verifica si hay una nueva contraseña y aplica el hash antes de actualizar
    if "password" in updated_fields:
        updated_fields["password"] = hash_password(updated_fields["password"])

    # Actualiza el usuario en la base de datos
    users_collection.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": updated_fields}
    )

    return {"message": "Usuario actualizado correctamente"}
