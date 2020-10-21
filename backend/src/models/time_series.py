from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Integer
from src.db.base_model import BaseModel


class TimeSeries(BaseModel):
    datetime = Column(DateTime, primary_key=True, index=True)
    symbol = Column(String, ForeignKey("stock.symbol"))
    low = Column(Float)
    high = Column(Float)
    open_p = Column(Float)
    close_p = Column(Float)
    volume = Column(Integer)