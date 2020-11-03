from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel as BaseSchema
from src.core.config import settings
from src.util.extended_types import Const


class UserBase(BaseSchema):
    username: str
    email: str  # TODO change this to EmailStr (e.g. i.p@gmail == ip@gmail)
    balance: float
    level: int
    exp: float
    last_reset: Optional[datetime]
    resets: int


class UserCreate(UserBase):
    uid: str
    balance: float = Const(settings.STARTING_BALANCE)
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


class LeaderboardUserBase(BaseSchema):
    username: str
    email: str
    level: int
    net_worth: float


class LeaderboardUserWithUid(LeaderboardUserBase):
    uid: str


class LeaderboardUserAPIout(LeaderboardUserBase):
    pass


class LeaderboardAPIout(BaseSchema):
    rankings: List[LeaderboardUserAPIout]
    user_ranking: int
