from pydantic import BaseModel, EmailStr
from typing import Optional
class TaskBase(BaseModel):
    title: str
    done: bool = False

class TaskCreate(TaskBase):
    pass

class TaskGet(TaskBase):
    id: int
    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str

class UserGet(UserBase):
    id: int
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str