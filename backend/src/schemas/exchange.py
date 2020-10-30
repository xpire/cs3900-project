import datetime as dt

from pydantic import BaseModel as BaseSchema
from pydantic import validator
from pytz import timezone


class ExchangeBase(BaseSchema):
    """
    Assumption, [start] and [end] times are on the same day, except [end] maybe at 0am
    """

    name: str
    open: dt.timedelta  # time since 0 o'clock of the day
    close: dt.timedelta  # time since 0 o'clock of the day
    timezone: str
    simulated: bool = False


class ExchangeInDBBase(ExchangeBase):
    class Config:
        orm_mode = True


class ExchangeFromDB(ExchangeInDBBase):
    pass


class ExchangeIntoDB(ExchangeInDBBase):
    pass
