from typing import Optional

from pydantic import BaseModel as BaseSchema
from pydantic import EmailStr, validator


class UserBase(BaseSchema):
    username: str
    email: str
    uuid: str


class UserCreate(UserBase):
    balance: float = 10000


class UserUpdate(UserBase):
    balance: float


class UserInDBBase(UserBase):
    balance: float

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    pass
