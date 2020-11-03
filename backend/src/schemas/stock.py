from datetime import timedelta

from pydantic import BaseModel as BaseSchema
from src.core.config import settings
from src.util.extended_types import Const


class TradingHoursInfo(BaseSchema):
    is_trading: bool
    open: timedelta
    close: timedelta


class StockBase(BaseSchema):
    symbol: str
    name: str
    exchange: str
    industry: str
    currency: str
    type: str


class StockAPIout(StockBase):
    pass


class StockRealTimeAPIout(StockBase):
    curr_day_close: float
    curr_day_open: float
    prev_day_close: float
    commission: float = Const(settings.COMMISSION_RATE)
    trading_hours_info: TradingHoursInfo
