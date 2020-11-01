from datetime import datetime
from typing import Optional

from pydantic import BaseModel as BaseSchema
from src.schemas.transaction import OrderType, TradeType
from src.util.extended_types import Const


class PendingOrder(BaseSchema):
    id: Optional[int]
    user_id: str
    symbol: str
    qty: int
    trade_type: TradeType
    order_type: OrderType
    timestamp: datetime

    class Config:
        orm_mode = True


class LimitOrder(PendingOrder):
    limit_price: float
    order_type = Const(OrderType.LIMIT)


class MarketOrder(PendingOrder):
    order_type = Const(OrderType.MARKET)
