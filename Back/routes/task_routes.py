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
        "carpeta": task.carpeta,
        "prioridad": task.prioridad,
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
                "terminado": task["terminado"],
                "prioridad": task.get("prioridad"),
                "carpeta": task.get("carpeta")
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
                "terminado": task["terminado"],
                "prioridad": task.get("prioridad"),
                "carpeta": task.get("carpeta")
            }
            for task in tasks
        ]
        return {"tasks": tasks_list}
    
    return {"message": "No hay tareas en el historial."}

@router.get("/prioridad/{prioridad}", status_code=status.HTTP_200_OK)
async def get_user_tasks(prioridad: str, user_id: str = Depends(get_user_id)):
    """Obtiene todas las tareas no terminadas del usuario autenticado con la prioridad especificada."""
    
    # Buscar las tareas en la colección de tareas que correspondan al user_id y la prioridad especificada
    tasks = await task_collection.find({"user_id": ObjectId(user_id), "prioridad": prioridad}).to_list(length=None)

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
                "prioridad": task.get("prioridad"),
                "carpeta": task.get("carpeta")               
            }
            for task in tasks
        ]
        return {"tasks": tasks_list}
    
    return {"message": "No hay tareas registradas para este usuario con esta prioridad."}



@router.put("/finished/{task_id}", status_code=status.HTTP_200_OK)
async def update_task_status(task_id: str, estado: bool, user_id: str = Depends(get_user_id)):
    """Permite cambiar el estado de 'terminado' de la tarea a True o False."""
    
    # Buscar la tarea por su ID
    task = await task_collection.find_one({"_id": ObjectId(task_id), "user_id": ObjectId(user_id)})
    
    # Verificar si la tarea existe
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # Actualizar la tarea con el estado indicado y la fecha de finalización solo si se marca como completada
    update_fields = {"terminado": estado}
    if estado:
        update_fields["fecha_finalizado"] = datetime.now()
    else:
        update_fields["fecha_finalizado"] = None

    await task_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_fields}
    )
    
    return {
        "message": f"Tarea {'completada' if estado else 'marcada como no completada'} con éxito",
    }

    
@router.put("/update/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(task_id: str, task_data: TaskUpdate, user_id: str = Depends(get_user_id)):
    """
    Actualiza cualquier campo de una tarea específica del usuario autenticado.
    """
    # Validar si la tarea existe y pertenece al usuario
    task = await task_collection.find_one({"_id": ObjectId(task_id), "user_id": ObjectId(user_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada o no pertenece al usuario")

    # Convertir datos de Pydantic a diccionario y excluir los valores nulos
    update_data = {k: v for k, v in task_data.dict(exclude_unset=True).items()}

    # Actualizar el campo `updated_at` automáticamente
    update_data["fecha_creación"] = datetime.utcnow()

    # Actualizar la tarea en la base de datos
    result = await task_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_data}
    )

    if result.modified_count == 1:
        return {"message": "Tarea actualizada con éxito"}
    else:
        raise HTTPException(status_code=400, detail="No se pudo actualizar la tarea")