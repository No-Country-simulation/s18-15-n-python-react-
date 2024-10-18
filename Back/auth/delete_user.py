from fastapi import APIRouter, HTTPException, Depends, status
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from config import MONGO_DETAILS
from dependencies import get_user_id 

# Conectar a MongoDB
client = MongoClient(MONGO_DETAILS)
db = client["Taskmanager"]
users_collection = db['users'] 
tasks_collection = db['tasks']

# Crear el router
router = APIRouter()

@router.delete("/users/me", status_code=status.HTTP_200_OK)
async def delete_user(current_user_id: str = Depends(get_user_id)):
    """Elimina el usuario autenticado y todas las tareas relacionadas."""
    object_id = ObjectId(current_user_id)  # Convertir el user_id a ObjectId

    # Intentar eliminar al usuario
    result = users_collection.delete_one({"_id": object_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    # Intentar eliminar las tareas relacionadas
    tasks_result = tasks_collection.delete_many({"user_id": object_id})
    
    if tasks_result.deleted_count == 0:
        return {"message": "Usuario eliminado correctamente. No se encontraron tareas relacionadas."}

    return {"message": f"Usuario y {tasks_result.deleted_count} tareas eliminados correctamente."}
