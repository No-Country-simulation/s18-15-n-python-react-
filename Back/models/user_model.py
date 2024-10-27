from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Schemas de usuario
class UserCreate(BaseModel):
    email: EmailStr
    password: Optional[str] = None  # No necesario para autenticación con Google
    first_name: str
    last_name: str
    profile_img: Optional[str] = None
    auth_provider: Optional[str] = "email"  # "email" o "google"
    google_id: Optional[str] = None  # ID único de Google
    email_verified: Optional[bool] = False  # Verificación de correo
    last_login: Optional[datetime] = None  # Última vez que el usuario inició sesión

class UserOut(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    profile_img: Optional[str]
    tasks: List[str]
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    
class UserUpdate(BaseModel):
    password: Optional[str] = None  
    first_name: Optional[str] = None  
    last_name: Optional[str] = None  
    profile_img: Optional[str] = None

