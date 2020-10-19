from typing import Optional

from pydantic import BaseModel as BaseSchema
from pydantic import Field

# TODO figure out a way to export these
# BaseModel
# Const = lambda x: Field(x, const=x)


class UserBase(BaseSchema):
    username: str
    email: str
    balance: float
    level: int
    exp: float


class UserCreate(UserBase):
    uid: str
    balance: float = Field(10000, const=10000)
    level: int = Field(1, const=1)
    exp: float = Field(0, const=0)


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    class Config:
        orm_mode = True


class User(UserInDBBase):
    exp_until_next_level: Optional[float]
    is_max_level: bool


# probably not needed?
class UserInDB(UserInDBBase):
    uid: str
