from pydantic import BaseModel as BaseSchema
from typing import Optional

class StockDataBase(BaseSchema):
    pass

class StockDataCreate(StockDataBase):
    pass

class StockDataUpdate(StockDataBase):
    pass

class StockDataInDBBase(StockDataBase):
    class Config:
        orm_mode = True

class StockData(StockDataInDBBase):
    pass

class StockDataInDB(StockDataInDBBase):
    pass