from fastapi import APIRouter, HTTPException, status, Depends, Response
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
from config import MONGO_DETAILS
from dependencies import *

from schemas.task import  taskDescription, taskEntetity
from starlette.status import HTTP_204_NO_CONTENT
from models.task_model import TaskCreate
from typing import List
from pymongo import MongoClient


# Conectar a la base de datos MongoDB usando motor
#client = AsyncIOMotorClient(MONGO_DETAILS)
client = MongoClient(MONGO_DETAILS)
db = client["Taskmanager"]
users_collection = db['users']
task_collection = db['tasks'] 

# Crear el router para las rutas de tareas
router = APIRouter()



#endpoint  para registrat una tarea
@router.post('/',  status_code=status.HTTP_201_CREATED,  tags=["tasks"])
async def create_task(task: TaskCreate):
    new_task=dict(task)

    result =   task_collection.insert_one(new_task)
    
   
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
    

#endpoint  para consultar todas las tareas en la bd
@router.get('/',  tags=["tasks"])
async def list_task():
   return taskEntetity(task_collection.find())


#endpoint  para consultar  una tarea por carpeta
@router.get('/carpeta/{category}',  tags=["tasks"])
async def task_by_category(category: str):

    result= task_collection.find({'carpeta': category})

    if(result==None):
        return "No se encontro esta carpeta"
    

#endpoint  para consultar  una tarea por estatus pendiente
@router.get('/pendientes',  tags=["tasks"])
async def task_by_pendiente():

    result= task_collection.find({'terminado': False})

    if(result==None):
        return "No se encontro esta carpeta"
    
    return taskEntetity(result)


#endpoint  para consultar  una tarea por historial
@router.get('/history',  tags=["tasks"])
async def task_by_history():

    result= task_collection.find({'terminado': True})

    if(result==None):
        return "No se encontro esta carpeta"
    
    return taskEntetity(result)

#endpoint  para consultar  una tarea por prioridad
@router.get('/prioridad/{prioridad}',  tags=["tasks"])
async def task_by_prioridad(prioridad: str):

    result= task_collection.find({'prioridad': prioridad})

    if(result==None):
        return "No se encontro esta carpeta"
    
    return taskEntetity(result)


#endpoint  para consultar  una tarea por id
@router.get('/{id}', tags=["tasks"])
async def task_by_id(id: str):
    if(id==None):
        return "Id esta vacio"
    return taskDescription(task_collection.find_one({"_id": ObjectId(id)}))


 
#endpoint  para modificar una tarea
@router.put('/{id}', response_model=TaskCreate, tags=["tasks"])
async def update_task(task: TaskCreate, id: str):
    if(id==None):
        return "Id esta vacio"
    response=task_collection.find_one_and_update({
        "_id": ObjectId(id)
    }, {
        "$set": dict(task)
    })
    return taskDescription(task_collection.find_one({"_id": ObjectId(id)}))


#endpoint para eliminar una tarea
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
async def delete_task(id: str):
    if(id==None):
        return "Id esta vacio"
    task_collection.find_one_and_delete({ "_id": ObjectId(id)})
    return Response(status_code=HTTP_204_NO_CONTENT)

