"""
Schema for portfolio's net worth time series
Primarily used for graphing purposes to track users position values
"""

from datetime import datetime
from typing import List

from pydantic import BaseModel as BaseSchema


class NetWorthTimeSeriesBase(BaseSchema):
    timestamp: datetime
    net_worth: float


class NetWorthTimeSeriesAPIout(BaseSchema):
    data: List[NetWorthTimeSeriesBase]
