from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    title: str
    done: bool = False


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    done: Optional[bool]=None


class TaskCreate(TaskBase):
    pass

class TaskGet(TaskBase):
    id: int
    class Config:
        from_attributes = True
