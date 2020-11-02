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


class PendingOrderAPIout(BaseSchema):
    id: int
    symbol: str
    qty: int
    limit_price: Optional[float]
    trade_type: TradeType
    order_type: OrderType
    timestamp: datetime
    exchange: str

    class Config:
        orm_mode = True
