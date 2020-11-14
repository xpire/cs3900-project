"""
Schema for stock exchange information
"""

import datetime as dt

from pydantic import BaseModel as BaseSchema


class Exchange(BaseSchema):
    name: str
    open: dt.timedelta  # time since 0 O'clock of the day
    close: dt.timedelta  # time since 0 O'clock of the day
    timezone: str
    simulated: bool = False
