import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URI")
SECRET_KEY = os.getenv("SECRET_KEY")
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

__all__ = [MONGO_DETAILS, SECRET_KEY, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI]
