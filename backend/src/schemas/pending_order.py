from datetime import datetime
from typing import Optional

from pydantic import BaseModel as BaseSchema
from src.schemas.transaction import OrderType, TradeType
from src.util.extended_types import Const

"""
TODO convention:
- DBin - into db
- DBout - out of db
- APIin - from api
- APIout - to api
"""


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
    exchange: str


class PendingOrderDBcreate(PendingOrderBase):
    id: Optional[int] = Const(None)


class LimitOrderDBcreate(PendingOrderDBcreate):
    limit_price: float


class MarketOrderDBcreate(PendingOrderDBcreate):
    limit_price: Optional[float] = Const(None)
