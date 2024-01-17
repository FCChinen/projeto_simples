from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class User(UserBase):
    username: str
    is_active: bool

    class Config:
        orm_mode = True


class UserCreate(User):
    password: str
