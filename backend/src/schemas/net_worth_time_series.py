from datetime import datetime
from typing import List

from pydantic import BaseModel as BaseSchema


class NetWorthTimeSeriesBase(BaseSchema):
    timestamp: datetime
    net_worth: float


class NetWorthTimeSeriesAPIout(BaseSchema):
    data: List[NetWorthTimeSeriesBase]
