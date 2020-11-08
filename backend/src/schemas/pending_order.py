"""
Schema for pending orders - Limit Orders and After Market Orders
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel as BaseSchema
from src.core.utilities import Const
from src.schemas.transaction import OrderType, TradeType


class PendingOrderBase(BaseSchema):
    id: Optional[int]
    symbol: str
    qty: int
    limit_price: Optional[float]
    trade_type: TradeType
    order_type: OrderType
    timestamp: datetime


class PendingOrderAPIout(PendingOrderBase):
    id: int
    name: str
    exchange: str


class PendingOrderDBcreate(PendingOrderBase):
    id: Optional[int] = Const(None)
    user_id: str


class LimitOrderDBcreate(PendingOrderDBcreate):
    limit_price: float


class MarketOrderDBcreate(PendingOrderDBcreate):
    limit_price: Optional[float] = Const(None)
