from fastapi import APIRouter, HTTPException, Depends, status
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from config import MONGO_DETAILS
from .oauth_verify import verify_token

# Conectar a MongoDB
client = MongoClient(MONGO_DETAILS)
db = client["Taskmanager"]
users_collection = db['users'] 
tasks_collection = db['tasks']

# Crear el router
router = APIRouter()

@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: str, current_user: dict = Depends(verify_token)):
    """Elimina un usuario y todas las tareas relacionadas."""
    try:
        object_id = ObjectId(user_id)  # Convertir el user_id a ObjectId
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de usuario inválido.")

    # Verificar si el usuario autenticado tiene permisos
    if str(object_id) != current_user["sub"]: 
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para eliminar este usuario."
        )

    # Intentar eliminar al usuario
    result = users_collection.delete_one({"_id": object_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    # Intentar eliminar las tareas relacionadas
    tasks_result = tasks_collection.delete_many({"user_id": object_id})
    
    if tasks_result.deleted_count == 0:
        return {"message": "Usuario eliminado correctamente. No se encontraron tareas relacionadas."}

    return {"message": f"Usuario y {tasks_result.deleted_count} tareas eliminados correctamente."}
