"""
Schema for each trade type that can be executed
"""

from datetime import datetime
from enum import Enum, auto
from typing import Any

from pydantic import BaseModel as BaseSchema
from pydantic import validator
from src.core.utilities import AutoName
from typing_extensions import Literal


class OrderType(str, AutoName):
    MARKET = auto()
    LIMIT = auto()


class TradeType(str, Enum):
    BUY = (True, True, True)
    SELL = (False, True, False)
    SHORT = (False, False, True)
    COVER = (True, False, False)

    def __new__(cls, is_buying, is_long, is_opening):
        obj = str.__new__(cls)
        obj._value_ = None
        obj.is_buying = is_buying
        obj.is_long = is_long
        obj.is_opening = is_opening
        return obj

    def __init__(self, *args):
        self._value_ = self._name_

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._value_ == other._value_
        return False

    def __hash__(self):
        return hash(self._value_)

    def __ne__(self, other):
        return not self == other


class TransactionBase(BaseSchema):
    symbol: str
    qty: int
    price: float
    timestamp: datetime
    order_type: OrderType
    trade_type: TradeType


class Transaction(TransactionBase):
    user: Any  # UserDM


class OpeningTransaction(Transaction):
    trade_type: Literal[TradeType.BUY, TradeType.SHORT]


class ClosingTransaction(Transaction):
    trade_type: Literal[TradeType.SELL, TradeType.COVER]
    profit: float
    profit_percentage: float


class TransactionDBcreate(TransactionBase):
    pass


class TransactionAPIout(TransactionBase):
    id: int
    name: str
    value: float = None
    is_cancelled: bool

    @validator("value", pre=True, always=True)
    def compute_value(cls, v, *, values, **kwargs):
        return values["price"] * values["qty"]
