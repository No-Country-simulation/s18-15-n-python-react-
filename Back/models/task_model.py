from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    fecha_termino: Optional[datetime] = None
    fecha_finalizado: Optional[datetime] = None
    terminado: bool = False
    carpeta: Optional[str] = None
    prioridad: Optional[str] = None

class TaskUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    fecha_termino: Optional[datetime] = None
    fecha_finalizado: Optional[datetime] = None
    terminado: bool = False
    carpeta: Optional[str] = None
    prioridad: Optional[str] = None
