from backend.src.db.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, String, Float, DateTime
from typing import TYPE_CHECKING


class StockData(BaseModel):
    datetime = Column(DateTime, primary_key=True, index=True)
    stock_symbol = Column(String, ForeignKey("stock.symbol"))
    low = Column(Float)
    high = Column(Float)
    open_p = Column(Float)
    close_p = Column(Float)