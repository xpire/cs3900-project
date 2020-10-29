import datetime as dt

from pydantic import BaseModel as BaseSchema
from pz import timezone


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
    timezone: timezone

    # pre validator


class ExchangeIntoDB(ExchangeInDBBase):
    pass
