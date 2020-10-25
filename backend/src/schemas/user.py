from datetime import datetime
from typing import Optional

from pydantic import BaseModel as BaseSchema
from src.util.extended_types import Const


class UserBase(BaseSchema):
    username: str
    email: str  # TODO change this to EmailStr (e.g. i.p@gmail == ip@gmail)
    balance: float
    level: int
    exp: float
    last_reset: datetime
    resets: int


class UserCreate(UserBase):
    uid: str
    balance: float = Const(10000)
    level: int = Const(1)
    exp: float = Const(0)
    resets: int = Const(0)


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


class TransactionBase(BaseSchema):
    user_id: str
    price: float
    action: str
    symbol: str
    amount: int


class TransactionCreate(TransactionBase):
    pass


class LimitOrderBase(BaseSchema):
    user_id: str
    symbol: str
    amount: int
    t_type: str
    price: float

class LimitOrderCreate(LimitOrderBase):
    pass

class LimitOrderDelete(LimitOrderBase): 
    pass
