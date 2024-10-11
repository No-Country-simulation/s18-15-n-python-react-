from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Schemas de usuario
class UserCreate(BaseModel):
    email: EmailStr
    password: Optional[str] = None  
    first_name: str
    last_name: str
    profile_img: Optional[str] = None
    auth_provider: Optional[str] = "email"  

class UserOut(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    profile_img: Optional[str]
    tasks: List[str]
    created_at: datetime
    updated_at: datetime
