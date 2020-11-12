from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel as BaseSchema
from src.schemas.pending_order import PendingOrderAPIout
from src.schemas.portfolio import PortfolioAPIout, PortfolioStatAPIout
from src.schemas.stock import StockRealTimeAPIout
from src.schemas.transaction import TransactionAPIout
from src.schemas.user import LeaderboardAPIout


class BasicDetail(BaseSchema):
    username: str
    email: str
    level: int
    exp: float
    exp_until_next_level: Optional[float]
    exp_threshold: Optional[float]
    is_max_level: bool
    last_reset: Optional[datetime]
    resets: int


class UserDetailAPIout(BaseSchema):
    basic: BasicDetail
    watchlist: List[StockRealTimeAPIout]
    orders: List[PendingOrderAPIout]
    transactions: List[TransactionAPIout]
    portfolio: PortfolioAPIout
    stats: PortfolioStatAPIout
    leaderboard: LeaderboardAPIout
