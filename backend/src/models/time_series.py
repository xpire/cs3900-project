from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from src.db.base_model import BaseModel


class TimeSeries(BaseModel):
    symbol = Column(String, ForeignKey("stock.symbol"), primary_key=True)
    datetime = Column(DateTime, index=True, primary_key=True)
    low = Column(Float)
    high = Column(Float)
    open_p = Column(Float)
    close_p = Column(Float)
    volume = Column(Integer)
