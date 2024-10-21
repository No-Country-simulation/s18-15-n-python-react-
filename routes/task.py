from fastapi import APIRouter, status, Response
from config.db import conn
from schemas.task import  taskDescription, taskEntetity
from models.task import Task
from starlette.status import HTTP_204_NO_CONTENT
from bson import ObjectId


task= APIRouter()


#endpoint  para consultar todas las tareas
@task.get('/tasks')
def list_task():
   return taskEntetity(conn.local.task.find())
 

#endpoint  para consultar  una tarea por id
@task.get('/task/{id}')
def task_by_id(id: str):
    return taskDescription(conn.local.task.find_one({"_id": ObjectId(id)}))


#endpoint  para registrat una tarea
@task.post('/task')
def create_task(task: Task):
    new_task=dict(task)
    response=conn.local.task.insert_one(new_task).inserted_id
    return taskEntetity(response)


#endpoint  para modificar una tarea
@task.put('/task/{id}')
def update_task(task: Task, id: str):
    response=conn.local.task.find_one_and_update({
        "_id": ObjectId(id)
    }, {
        "$set": dict(task)
    })
    return taskEntetity(conn.local.user.find_one({"_id": ObjectId(id)}))


#endpoint para eliminar una tarea
@task.delete('/task/{id}')
def delete_task(id: str):
    conn.local.task.find_one_and_delete({ "_id": ObjectId(id)})
    return Response(status_code=HTTP_204_NO_CONTENT)

