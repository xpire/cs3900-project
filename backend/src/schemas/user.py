"""
Schema for user information and statistics
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel as BaseSchema
from src.core.config import settings
from src.core.utilities import Const


class UserBase(BaseSchema):
    username: str
    email: str
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


class UserAPIout(UserBase):
    exp_until_next_level: Optional[float]
    exp_threshold: Optional[float]
    is_max_level: bool


class UserDBout(UserBase):
    uid: str

    class Config:
        orm_mode = True


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
