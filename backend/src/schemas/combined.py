from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel as BaseSchema
from src.schemas.notification import NotifEventType
from src.schemas.pending_order import PendingOrderAPIout
from src.schemas.portfolio import PortfolioAPIout, PortfolioStatAPIout
from src.schemas.stock import StockAPIout
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


class NotificationAPIout(BaseSchema):
    id: int
    title: str
    content: str = ""
    event_type: NotifEventType


class UserDetailAPIout(BaseSchema):
    basic: BasicDetail
    watchlist: List[StockAPIout]
    orders: List[PendingOrderAPIout]
    transactions: List[TransactionAPIout]
    portfolio: PortfolioAPIout
    stats: PortfolioStatAPIout
    leaderboard: LeaderboardAPIout
    notifications: List[NotificationAPIout]
