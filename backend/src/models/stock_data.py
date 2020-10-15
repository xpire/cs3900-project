from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Float, DateTime

from backend.src.db.base_class import Base

# if TYPE_CHECKING:
#     from .stock import Stock

class StockData(Base):
    id = Column(DateTime, primary_key = True, index = True)
    stock_symbol = Column(String, ForeignKey('stock.symbol')) 
    low = Column(Float)
    high = Column(Float)
    open_p = Column(Float)
    close_p = Column(Float)

