from pydantic import BaseModel, Field
from typing import Optional


class UserBase(BaseModel):
    email: str


class User(UserBase):
    id: int
    username: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    username: str
    password: str


class UpdateUser(BaseModel):
    id: int
    email: Optional[str] = Field(None)
    username: Optional[str] = Field(None)
    password: Optional[str] = Field(None)
