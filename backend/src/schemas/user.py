from pydantic import BaseModel as BaseSchema, EmailStr, validator
from typing import Optional

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
