from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, timedelta
from models import TaskCreate
from config import MONGO_DETAILS
from dependencies import get_user_id, convert_to_utc

# Conectar a la base de datos MongoDB usando motor
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client["Taskmanager"]
users_collection = db['users']
task_collection = db['tasks'] 

# Crear el router para las rutas de tareas
router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, user_id: str = Depends(get_user_id)): 
    """Registra una nueva tarea y programa una notificación."""    
    # Buscar el usuario en la base de datos
    user = await users_collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    # Obtener la zona horaria del usuario
    timezone_str = user['timezone']

    # Calcular el `notification_time`
    notification_time = task.notification_time
    if not notification_time and task.fecha_termino:
        # Si no se especifica, la notificación será el mismo día a las 8 AM en la zona horaria del usuario
        local_dt = datetime.combine(task.fecha_termino.date(), datetime.min.time()).replace(hour=8, minute=0)
        # Convertir la hora local a UTC para guardar en la base de datos
        notification_time = convert_to_utc(local_dt, timezone_str)
    else:
        # Si se proporciona notification_time, asegúrate de que esté en la zona horaria local y conviértelo a UTC
        notification_time = convert_to_utc(notification_time, timezone_str)

    # Validar y ajustar fechas antes de guardar
    fecha_creacion = datetime.now(timezone.utc)
    fecha_termino = task.fecha_termino if task.fecha_termino else None
    
    # Crear la tarea
    new_task = {
        "title": task.title,
        "description": task.description,
        "fecha_creacion": fecha_creacion,  # Guardar en UTC
        "fecha_termino": fecha_termino,     # Guardar en UTC
        "fecha_finalizado": None,
        "terminado": False,
        "user_id": ObjectId(user_id),
        "notification_time": notification_time,  # Guardar en UTC
        "notifiqued": task.notifiqued
    }

    # Imprimir para depuración
    print("Nueva tarea a guardar:", new_task)

    # Insertar la nueva tarea
    result = await task_collection.insert_one(new_task)

    if result.inserted_id:
        return {
            "message": "Tarea registrada correctamente.",
            "task_id": str(result.inserted_id)
        }
    else:
        raise HTTPException(status_code=500, detail="Error al registrar la tarea.")

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
                "terminado": task["terminado"],
                "notification_time": task.get("notification_time"),
                "notifiqued": task.get("notifiqued", False)
            }
            for task in tasks
        ]
        return {"tasks": tasks_list}
    
    return {"message": "No hay tareas registradas para este usuario."}

@router.get("/history", status_code=status.HTTP_200_OK)
async def get_user_completed_tasks(user_id: str = Depends(get_user_id)):
    """Obtiene todas las tareas terminadas del usuario autenticado."""    
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
async def get_all_user_tasks(user_id: str = Depends(get_user_id)):
    """Obtiene todas las tareas del usuario autenticado."""    
    # Buscar las tareas en la colección de tareas que correspondan al user_id
    tasks = await task_collection.find({"user_id": ObjectId(user_id)}).to_list(length=None)

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
