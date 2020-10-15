from typing import Optional
from pydantic import BaseModel


# Shared properties
class StockDataBase(BaseModel):
    pass


# Properties to receive on item creation
class StockDataCreate(StockDataBase):
    pass


class StockDataUpdate(StockDataBase):
    """
    Not used, should not be updating exisiting stock information.
    """

    pass


class StockDataRet(StockDataBase):
    pass


# Properties shared by models stored in DB
class StockDataInDBBase(StockDataBase):
    pass

    class Config:
        orm_mode = True