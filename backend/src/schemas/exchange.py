import datetime as dt

from pydantic import BaseModel as BaseSchema
from pydantic import validator
from pytz import timezone


class ExchangeBase(BaseSchema):
    name: str
    start: dt.time
    end: dt.time
    timezone: str
    simulated: bool = False


class ExchangeInDBBase(ExchangeBase):
    class Config:
        orm_mode = True


class ExchangeFromDB(ExchangeInDBBase):
    pass


class ExchangeIntoDB(ExchangeInDBBase):
    pass
