from fastapi import APIRouter, HTTPException, status, Depends, Response
from bson import ObjectId
from config import MONGO_DETAILS
from dependencies import get_user_id

from schemas.task import taskDescription, taskEntetity
from models.task_model import TaskCreate, TaskUpdate
from pymongo import MongoClient

# Conectar a la base de datos MongoDB usando motor
client = MongoClient(MONGO_DETAILS)
db = client["Taskmanager"]
task_collection = db['tasks']

# Crear el router para las rutas de tareas
router = APIRouter()

# Endpoint para registrar una tarea
@router.post('/', status_code=status.HTTP_201_CREATED, tags=["tasks"])
async def create_task(task: TaskCreate, user_id: str = Depends(get_user_id)):
    new_task = dict(task)
    new_task["user_id"] = user_id
    result = task_collection.insert_one(new_task)

    if result.inserted_id:
        return {"message": "Tarea registrada correctamente.", "task_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al registrar la tarea.")

# Endpoint para listar todas las tareas del usuario
@router.get('/', tags=["tasks"])
async def list_tasks(user_id: str = Depends(get_user_id)):
    tasks = list(task_collection.find({"user_id": user_id}))
    return taskEntetity(tasks)

# Endpoint para consultar tareas por carpeta
@router.get('/carpeta/{category}', tags=["tasks"])
async def tasks_by_category(category: str, user_id: str = Depends(get_user_id)):
    tasks = list(task_collection.find({'user_id': user_id, 'carpeta': category}))
    if not tasks:
        return {"message": "No se encontró ninguna tarea en esta carpeta"}
    return taskEntetity(tasks)

# Endpoint para consultar tareas pendientes
@router.get('/pendientes', tags=["tasks"])
async def tasks_by_pending(user_id: str = Depends(get_user_id)):
    tasks = list(task_collection.find({'user_id': user_id, 'terminado': False}))
    if not tasks:
        return {"message": "No se encontraron tareas pendientes"}
    return taskEntetity(tasks)

# Endpoint para consultar tareas finalizadas
@router.get('/history', tags=["tasks"])
async def tasks_by_history(user_id: str = Depends(get_user_id)):
    tasks = list(task_collection.find({'user_id': user_id, 'terminado': True}))
    if not tasks:
        return {"message": "No se encontraron tareas finalizadas"}
    return taskEntetity(tasks)

# Endpoint para consultar tareas por prioridad
@router.get('/prioridad/{prioridad}', tags=["tasks"])
async def tasks_by_priority(prioridad: str, user_id: str = Depends(get_user_id)):
    tasks = list(task_collection.find({'user_id': user_id, 'prioridad': prioridad}))
    if not tasks:
        return {"message": "No se encontraron tareas con esa prioridad"}
    return taskEntetity(tasks)

# Endpoint para consultar una tarea por ID
@router.get('/{id}', tags=["tasks"])
async def task_by_id(id: str, user_id: str = Depends(get_user_id)):
    task = task_collection.find_one({"_id": ObjectId(id), "user_id": user_id})
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada o acceso no autorizado")
    return taskDescription(task)

# Endpoint para modificar una tarea
@router.put('/{id}', response_model=TaskUpdate, tags=["tasks"])
async def update_task(task: TaskUpdate, id: str, user_id: str = Depends(get_user_id)):
    updated_fields = task.model_dump(exclude_unset=True)
    existing_task = task_collection.find_one({"_id": ObjectId(id), "user_id": user_id})
    
    if not existing_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada o acceso no autorizado")

    task_collection.find_one_and_update(
        {"_id": ObjectId(id), "user_id": user_id},
        {"$set": updated_fields}
    )

    return taskDescription(task_collection.find_one({"_id": ObjectId(id)}))

# Endpoint para eliminar una tarea
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
async def delete_task(id: str, user_id: str = Depends(get_user_id)):
    task = task_collection.find_one({"_id": ObjectId(id), "user_id": user_id})
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada o acceso no autorizado")

    task_collection.find_one_and_delete({"_id": ObjectId(id), "user_id": user_id})
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Endpoint para cambiar el estado de "terminado"
@router.patch('/done/{id}', tags=["tasks"])
async def toggle_task_status(id: str, user_id: str = Depends(get_user_id)):
    task = task_collection.find_one({"_id": ObjectId(id), "user_id": user_id})
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada o acceso no autorizado")

    new_status = not task.get("terminado", False)
    task_collection.find_one_and_update(
        {"_id": ObjectId(id), "user_id": user_id},
        {"$set": {"terminado": new_status}}
    )

    return {"message": "Estado de tarea actualizado", "terminado": new_status}
