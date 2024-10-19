from fastapi import FastAPI
from routes.task import task


app= FastAPI()

#incluimos las rutas desde el archivo task.py en la carpeta routes
app.include_router(task)



