from typing import Optional

from pydantic import BaseModel as BaseSchema


class StockBase(BaseSchema):
    pass


class StockCreate(StockBase):
    pass


class StockUpdate(StockBase):
    pass


class StockInDBBase(StockBase):
    class Config:
        orm_mode = True


class Stock(StockInDBBase):
    pass


class StockInDB(StockInDBBase):
    pass
