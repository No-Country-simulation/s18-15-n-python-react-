from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    id: Optional[str]
    title: str
    description: Optional[str] = None
    fecha_termino: Optional[datetime] = None
    fecha_finalizado: Optional[datetime] = None
    carpeta: Optional[str] = None
    prioridad: Optional[str] = None
    terminado: bool = False

    """
class TaskCreate(BaseModel):
    id: Optional[str]
    name: str
    description: str
    date_limit: str
    date_finish: str
    priority: str
    urgency: str
    category: str
    remindir:str

"""

