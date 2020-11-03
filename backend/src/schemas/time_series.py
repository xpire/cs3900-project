from datetime import date
from typing import Optional

from pydantic import BaseModel as BaseSchema


class TimeSeriesBase(BaseSchema):
    date: date
    symbol: str
    low: float
    high: float
    open: float
    close: float
    volume: int


class TimeSeriesDBcreate(TimeSeriesBase):
    pass


class TimeSeriesAPIout(TimeSeriesBase):

    class Config:
        orm_mode=True
