from datetime import datetime
from enum import auto
from typing import Any

from pydantic import BaseModel as BaseSchema
from pydantic import validator
from src.core.utilities import AutoName
from typing_extensions import Literal


class OrderType(str, AutoName):
    MARKET = auto()
    LIMIT = auto()


class TradeType(str, AutoName):
    BUY = auto()
    SELL = auto()
    SHORT = auto()
    COVER = auto()


class Transaction(BaseSchema):
    user: Any  # UserDM
    order_type: OrderType
    trade_type: TradeType
    symbol: str
    quantity: int
    brokerage_fee: float
    trade_timestamp: datetime


class OpeningTransaction(Transaction):
    trade_type: Literal[TradeType.BUY, TradeType.SHORT]


class ClosingTransaction(Transaction):
    trade_type: Literal[TradeType.SELL, TradeType.COVER]
    profit: float
    profit_percentage: float


class TransactionAPIout(BaseSchema):
    symbol: str
    name: str
    qty: int
    price: float
    value: float = None
    trade_type: TradeType
    timestamp: datetime

    @validator("value", pre=True)
    def compute_value(cls, v, *, values, **kwargs):
        return values["price"] * values["qty"]
