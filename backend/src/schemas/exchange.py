import datetime as dt

from pydantic import BaseModel as BaseSchema
from pydantic import validator
from pytz import timezone


class ExchangeBase(BaseSchema):
    """
    Assumption, [start] and [end] times are on the same day, except [end] maybe at 0am
    """

    name: str
    start: dt.timedelta  # time since 0 o'clock of the day
    end: dt.timedelta  # time since 0 o'clock of the day
    timezone: str
    simulated: bool = False

    # def is_before_open(self, time):
    #     return time < self.start

    # def is_after_close(self, time):
    #     return False if self.end == dt.time(0) else time >= self.start


class ExchangeInDBBase(ExchangeBase):
    class Config:
        orm_mode = True


class ExchangeFromDB(ExchangeInDBBase):
    pass


class ExchangeIntoDB(ExchangeInDBBase):
    pass
