from fastapi import FastAPI
from routes.task import task


app= FastAPI(
     title="FastAPI & Mongo CRUD",
     description="this is a simple REST API using fastapi and mongodb",
     version="0.0.1"

)

#incluimos las rutas desde el archivo task.py en la carpeta routes
app.include_router(task)



