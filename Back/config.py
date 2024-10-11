import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URI")
JWT_SECRET = os.getenv("JWT_SECRET")
