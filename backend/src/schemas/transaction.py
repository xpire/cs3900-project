from datetime import datetime
from enum import auto
from typing import Any

from pydantic import BaseModel as BaseSchema
from src.util.auto_name_enum import AutoName
from src.util.extended_types import Const
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
