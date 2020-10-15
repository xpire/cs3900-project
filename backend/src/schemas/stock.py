from typing import Optional

from pydantic import BaseModel as BaseSchema


# Shared properties
class StockBase(BaseSchema):
    pass


# Properties to receive on item creation
class StockCreate(StockBase):
    pass


# Properties to receive on item update
class StockUpdate(StockBase):
    pass


# Properties shared by models stored in DB
class StockInDBBase(StockBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class StockRet(StockInDBBase):
    pass


# Properties properties stored in DB
# class ItemInDB(stockInDBBase):
#     pass
