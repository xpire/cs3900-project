from typing import Optional

from pydantic import BaseModel, EmailStr, validator 


# Shared properties
class UserBase(BaseModel):
    pass


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    email: str
    balance: float
    token: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    balance: float


class UserInDBBase(UserBase):
    pass
    class Config:
        orm_mode = True


# Additional properties to return via API
class UserRet(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    pass
