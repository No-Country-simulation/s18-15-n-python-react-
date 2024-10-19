from fastapi import APIRouter
from config.db import conn
from schemas.task import taskDescription, taskEntetity
from models.task import Task

task= APIRouter()



@task.get('/tasks')
def list_task():
   return taskEntetity(conn.local.task.find())


@task.post('/task')
def create_task(task: Task):
    new_task=dict(task)
    response=conn.local.task.insert_one(new_task)
    return str(response)
