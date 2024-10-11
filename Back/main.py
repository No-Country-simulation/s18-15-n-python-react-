from fastapi import FastAPI
from Back.db import init_db
from Back.models import UserCreate, UserOut, TaskCreate 

app = FastAPI()

@app.on_event("startup")
async def startup_db():
    await init_db()

#importar rutas
