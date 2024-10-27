from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DETAILS

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.Taskmanager

# Colecciones
user_collection = database.get_collection("users")
task_collection = database.get_collection("tasks")

async def init_db():
    
    await user_collection.create_index("email", unique=True)
    await task_collection.create_index("user_id")
    print("Colecciones y índices inicializados.")
