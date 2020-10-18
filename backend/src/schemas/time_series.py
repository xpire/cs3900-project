from pydantic import BaseModel as BaseSchema
from typing import Optional


class TimeSeriesBase(BaseSchema):
    pass


class TimeSeriesCreate(TimeSeriesBase):
    pass


class TimeSeriesUpdate(TimeSeriesBase):
    pass


class TimeSeriesInDBBase(TimeSeriesBase):
    class Config:
        orm_mode = True


class TimeSeries(TimeSeriesInDBBase):
    pass


class TimeSeriesInDB(TimeSeriesInDBBase):
    pass