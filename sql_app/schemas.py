from typing import Union
from pydantic import BaseModel

class MyBaseModel(BaseModel):
    class Config:
        orm_mode = True

class ProjectBase(MyBaseModel):
    title: str
    description: Union[str, None] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    owner_id: int

class UserBase(MyBaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    projects: list[Project] = []
