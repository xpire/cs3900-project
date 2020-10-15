from typing import Optional

from pydantic import BaseModel as BaseSchema, EmailStr, validator


# Shared properties
class UserBase(BaseSchema):
    username: str
    email: str
    uuid: str


# Properties to receive via API on creation
class UserCreate(UserBase):
    balance: float = 10000
    pass


# Properties to receive via API on update
class UserUpdate(UserBase):
    balance: float


class UserInDBBase(UserBase):
    balance: float

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    pass
