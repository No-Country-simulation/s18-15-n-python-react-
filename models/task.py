from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    id: Optional[str]
    name: str
    description: str
    date_limit: str
    date_finish: str
    priority: str
    urgency: str
    category: str
    remindir:str