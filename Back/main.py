from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from auth import router as auth_router
from routes import router as routes_router
from db import init_db
from contextlib import asynccontextmanager
from config import SECRET_KEY
from dependencies import revisar_tareas_vencimiento
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Inicializar el programador
scheduler = AsyncIOScheduler()

# Evento de inicialización de base de datos
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Base de datos inicializada")
    
    # Iniciar el programador y añadir el trabajo para verificar tareas
    scheduler.add_job(revisar_tareas_vencimiento, 'interval', minutes=10)
    scheduler.start()
    print("Programador iniciado y verificando tareas.")
    
    yield

    # Detener el programador al cerrar la aplicación
    scheduler.shutdown()
    print("Programador detenido.")

# Crear la aplicación de FastAPI
def create_app() -> FastAPI:
    # Inicialización de FastAPI
    app = FastAPI(lifespan=lifespan)

    # Middleware de sesión
    app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

    # Registrar las rutas de autenticación
    app.include_router(auth_router, prefix="/auth") 

    # Registrar rutas CRUD para tareas
    app.include_router(routes_router, prefix="/task") 

    # Otras rutas
    @app.get("/")
    async def welcome():
        """Mensaje de bienvenida en la raíz."""
        return {"message": "Welcome"}

    return app

# En Render, FastAPI espera una variable llamada app
app = create_app()
