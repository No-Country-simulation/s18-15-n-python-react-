from fastapi import APIRouter, status, Response
from config.db import conn
from schemas.task import  taskDescription, taskEntetity
from models.task import Task
from starlette.status import HTTP_204_NO_CONTENT
from bson import ObjectId


task= APIRouter()


#endpoint  para consultar todas las tareas
@task.get('/tasks',  tags=["tasks"])
def list_task():
   return taskEntetity(conn.local.task.find())
 

#endpoint  para consultar  una tarea por id
@task.get('/task/{id}', tags=["tasks"])
def task_by_id(id: str):
    if(id==None):
        return "Id esta vacio"
    return taskDescription(conn.local.task.find_one({"_id": ObjectId(id)}))


#endpoint  para consultar  una tarea por categoria
@task.get('/task/category/{category}',  tags=["tasks"])
def task_by_category(category: str):
    if(id==None):
        return "Categoria esta vacia"
    resp= conn.local.task.find_one({'category': category})
    if resp == None:
        return conn.local.task.find_one({'category': category})
    
    return taskDescription(conn.local.task.find_one({'category': category}))
    

#endpoint  para registrat una tarea
@task.post('/task',  tags=["tasks"])
def create_task(task: Task):
    new_task=dict(task)
    response=conn.local.task.insert_one(new_task).inserted_id
    return taskEntetity(response)


#endpoint  para modificar una tarea
@task.put('/task/{id}', response_model=Task, tags=["tasks"])
def update_task(task: Task, id: str):
    if(id==None):
        return "Id esta vacio"
    response=conn.local.task.find_one_and_update({
        "_id": ObjectId(id)
    }, {
        "$set": dict(task)
    })
    return taskEntetity(conn.local.user.find_one({"_id": ObjectId(id)}))


#endpoint para eliminar una tarea
@task.delete('/task/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(id: str):
    if(id==None):
        return "Id esta vacio"
    conn.local.task.find_one_and_delete({ "_id": ObjectId(id)})
    return Response(status_code=HTTP_204_NO_CONTENT)

