from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    fecha_creacion: datetime
    fecha_termino: Optional[datetime]
    fecha_finalizado: Optional[datetime] = None
    terminado: bool = False
