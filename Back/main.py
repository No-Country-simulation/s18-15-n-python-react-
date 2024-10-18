from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from auth import router as auth_router 
from db import init_db
from contextlib import asynccontextmanager
from config import SECRET_KEY

# Evento de inicialización de base de datos
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Base de datos inicializada")
    yield

# Inicialización de FastAPI
app = FastAPI(lifespan=lifespan)

# Middleware de sesión
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Registrar las rutas de autenticación
app.include_router(auth_router, prefix="/auth") 

# Registrar rutas crud para tareas



# Otras rutas
@app.get("/")
async def welcome():
    """Mensaje de bienvenida en la raíz."""
    return {"message": "Welcome"}
