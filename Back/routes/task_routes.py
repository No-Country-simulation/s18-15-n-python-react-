from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
import pymongo
from datetime import datetime, timezone
from models import TaskCreate
from ..auth.oauth_verify import verify_token  
from config import MONGO_DETAILS

# Conectar a la base de datos MongoDB
client = pymongo.MongoClient(MONGO_DETAILS)
db = client["Taskmanager"]
users_collection = db['users']
task_collection = db['tasks'] 

# Crear el router para las rutas de tareas
router = APIRouter()

@router.post("/task", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, token_data: dict = Depends(verify_token)): 
    """Registra una nueva tarea en la colección de tareas y la vincula al usuario autenticado."""

    user_id = token_data['sub']  # Extraemos el user_id del token JWT

    # Buscar el usuario en la base de datos
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    # Crear la nueva tarea usando el modelo TaskCreate
    new_task = {
        "user_id": ObjectId(user_id),  # Vincular tarea con el usuario
        "title": task.title,
        "description": task.description,
        "fecha_creacion": datetime.now(timezone.utc),
        "fecha_termino": task.fecha_termino,
        "fecha_finalizado": None,
        "terminado": False
    }

    # Insertar la nueva tarea en la colección de tareas
    result = await task_collection.insert_one(new_task)

    if result.inserted_id:
        return {
            "message": "Tarea registrada correctamente.",
            "task_id": str(result.inserted_id)  # Retornar el ID de la tarea creada
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar la tarea."
        )
