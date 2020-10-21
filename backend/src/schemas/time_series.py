from datetime import datetime
from typing import Optional

from pydantic import BaseModel as BaseSchema


class TimeSeriesBase(BaseSchema):
    datetime: datetime
    symbol: str
    low: float
    high: float
    open_p: float
    close_p: float
    volume: int


class TimeSeriesCreate(TimeSeriesBase):
    pass
