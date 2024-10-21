from pydantic import BaseModel

class Task(BaseModel):
    name: str
    description: str
    date_limit: str
    date_finish: str
    priority: str
    urgency: str
    category: str
    remindir:str