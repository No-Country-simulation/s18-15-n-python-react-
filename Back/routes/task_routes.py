from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
from models import TaskCreate
from config import MONGO_DETAILS
from dependencies import *

# Conectar a la base de datos MongoDB usando motor
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client["Taskmanager"]
users_collection = db['users']
task_collection = db['tasks'] 

# Crear el router para las rutas de tareas
router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, user_id: str = Depends(get_user_id)): 
    """Registra una nueva tarea en la colección de tareas y la vincula al usuario autenticado."""

    # Buscar el usuario en la base de datos de manera asíncrona
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    # Crear la nueva tarea usando el modelo TaskCreate
    new_task = {
        "title": task.title,
        "description": task.description,
        "fecha_creacion": datetime.now(timezone.utc),
        "fecha_termino": task.fecha_termino,
        "fecha_finalizado": None,
        "terminado": False,
        "user_id": ObjectId(user_id)  # Relacionar la tarea con el usuario
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


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_tasks(user_id: str = Depends(get_user_id)):
    """Obtiene todas las tareas no terminadas del usuario autenticado."""
    
    # Buscar las tareas en la colección de tareas que correspondan al user_id y que no estén terminadas
    tasks = await task_collection.find({"user_id": ObjectId(user_id), "terminado": False}).to_list(length=None)

    if tasks:
        # Transformar las tareas a una lista
        tasks_list = [
            {
                "id": str(task["_id"]),
                "title": task["title"],
                "description": task.get("description"),
                "fecha_creacion": task["fecha_creacion"],
                "fecha_termino": task.get("fecha_termino"),
                "fecha_finalizado": task.get("fecha_finalizado"),
                "terminado": task["terminado"]
            }
            for task in tasks
        ]
        return {"tasks": tasks_list}
    
    return {"message": "No hay tareas registradas para este usuario."}


@router.get("/history", status_code=status.HTTP_200_OK)

async def get_user_tasks(user_id: str = Depends(get_user_id)):
    """Obtiene todas las tareas no terminadas del usuario autenticado."""
    
    # Buscar las tareas en la colección de tareas que correspondan al user_id y estén terminadas
    tasks = await task_collection.find({"user_id": ObjectId(user_id), "terminado": True}).to_list(length=None)

    if tasks:
        # Transformar las tareas a una lista
        tasks_list = [
            {
                "id": str(task["_id"]),
                "title": task["title"],
                "description": task.get("description"),
                "fecha_creacion": task["fecha_creacion"],
                "fecha_termino": task.get("fecha_termino"),
                "fecha_finalizado": task.get("fecha_finalizado"),
                "terminado": task["terminado"]
            }
            for task in tasks
        ]
        return {"tasks": tasks_list}
    
    return {"message": "No hay tareas en el historial."}

@router.get("/all", status_code=status.HTTP_200_OK)
async def get_user_tasks(user_id: str = Depends(get_user_id)):
    """Obtiene todas las tareas no terminadas del usuario autenticado."""
    
    # Buscar las tareas en la colección de tareas que correspondan al user_id y que no estén terminadas
    tasks = await task_collection.find({"user_id": ObjectId(user_id),}).to_list(length=None)

    if tasks:
        # Transformar las tareas a una lista
        tasks_list = [
            {
                "id": str(task["_id"]),
                "title": task["title"],
                "description": task.get("description"),
                "fecha_creacion": task["fecha_creacion"],
                "fecha_termino": task.get("fecha_termino"),
                "fecha_finalizado": task.get("fecha_finalizado"),
                "terminado": task["terminado"]
            }
            for task in tasks
        ]
        return {"tasks": tasks_list}
    
    return {"message": "No hay tareas registradas para este usuario."}