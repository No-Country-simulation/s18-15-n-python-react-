from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
from models import TaskCreate, TaskUpdate
from config import MONGO_DETAILS
from dependencies import get_user_id

# Conectar a la base de datos MongoDB usando motor
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client["Taskmanager"]
users_collection = db['users']
task_collection = db['tasks'] 

# Crear el router para las rutas de tareas
router = APIRouter()

async def get_user(user_id: str):
    """Buscar el usuario en la base de datos."""
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user

async def format_tasks(tasks):
    """Transformar la lista de tareas en el formato adecuado para la respuesta."""
    return [
        {
            "id": str(task["_id"]),
            "title": task["title"],
            "description": task.get("description"),
            "fecha_creacion": task["fecha_creacion"],
            "fecha_termino": task.get("fecha_termino"),
            "fecha_finalizado": task.get("fecha_finalizado"),
            "terminado": task["terminado"],
            "prioridad": task.get("prioridad"),
            "carpeta": task.get("carpeta")
        }
        for task in tasks
    ]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, user_id: str = Depends(get_user_id)): 
    """Registra una nueva tarea en la colección de tareas y la vincula al usuario autenticado."""
    
    await get_user(user_id)  # Verifica la existencia del usuario
    
    new_task = {
        "title": task.title,
        "description": task.description,
        "fecha_creacion": datetime.now(timezone.utc),
        "fecha_termino": task.fecha_termino,
        "fecha_finalizado": None,
        "terminado": False,
        "carpeta": task.carpeta,
        "prioridad": task.prioridad,
        "user_id": ObjectId(user_id)  # Relacionar la tarea con el usuario
    }

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
    tasks = await task_collection.find({"user_id": ObjectId(user_id), "terminado": False}).to_list(length=None)
    tasks_list = await format_tasks(tasks) if tasks else []
    return {"tasks": tasks_list} if tasks_list else {"message": "No hay tareas registradas para este usuario."}

@router.get("/history", status_code=status.HTTP_200_OK)
async def get_user_task_history(user_id: str = Depends(get_user_id)):
    """Obtiene todas las tareas terminadas del usuario autenticado."""
    tasks = await task_collection.find({"user_id": ObjectId(user_id), "terminado": True}).to_list(length=None)
    tasks_list = await format_tasks(tasks) if tasks else []
    return {"tasks": tasks_list} if tasks_list else {"message": "No hay tareas en el historial."}

@router.get("/prioridad/{prioridad}", status_code=status.HTTP_200_OK)
async def get_user_tasks_by_priority(prioridad: str, user_id: str = Depends(get_user_id)):
    """Obtiene todas las tareas no terminadas del usuario autenticado con la prioridad especificada."""
    tasks = await task_collection.find({"user_id": ObjectId(user_id), "prioridad": prioridad, "terminado": False}).to_list(length=None)
    tasks_list = await format_tasks(tasks) if tasks else []
    return {"tasks": tasks_list} if tasks_list else {"message": "No hay tareas registradas para este usuario con esta prioridad."}

@router.get("/carpeta/{carpeta}", status_code=status.HTTP_200_OK)
async def get_user_tasks_by_folder(carpeta: str, user_id: str = Depends(get_user_id)):
    """Obtiene todas las tareas no terminadas del usuario autenticado con la carpeta especificada."""
    tasks = await task_collection.find({"user_id": ObjectId(user_id), "carpeta": carpeta}).to_list(length=None)
    tasks_list = await format_tasks(tasks) if tasks else []
    return {"tasks": tasks_list} if tasks_list else {"message": f"No existe la carpeta {carpeta}."}

@router.put("/finished/{task_id}", status_code=status.HTTP_200_OK)
async def update_task_status(task_id: str, estado: bool, user_id: str = Depends(get_user_id)):
    """Permite cambiar el estado de 'terminado' de la tarea a True o False."""
    task = await task_collection.find_one({"_id": ObjectId(task_id), "user_id": ObjectId(user_id)})
    
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    update_fields = {"terminado": estado}
    if estado:
        update_fields["fecha_finalizado"] = datetime.now()
    else:
        update_fields["fecha_finalizado"] = None

    await task_collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_fields})
    
    return {"message": f"Tarea {'completada' if estado else 'marcada como no completada'} con éxito"}

@router.put("/update/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(task_id: str, task_data: TaskUpdate, user_id: str = Depends(get_user_id)):
    """Actualiza cualquier campo de una tarea específica del usuario autenticado."""
    task = await task_collection.find_one({"_id": ObjectId(task_id), "user_id": ObjectId(user_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada o no pertenece al usuario")

    update_data = {k: v for k, v in task_data.dict(exclude_unset=True).items()}
    update_data["fecha_creacion"] = datetime.utcnow()

    result = await task_collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})

    if result.modified_count == 1:
        return {"message": "Tarea actualizada con éxito"}
    else:
        raise HTTPException(status_code=400, detail="No se pudo actualizar la tarea")
