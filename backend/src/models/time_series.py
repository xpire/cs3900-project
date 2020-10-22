from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from src.db.base_model import BaseModel


class TimeSeries(BaseModel):
    datetime = Column(Date, primary_key=True, index=True)
    symbol = Column(String, ForeignKey("stock.symbol"), primary_key=True)
    low = Column(Float)
    high = Column(Float)
    open_p = Column(Float)
    close_p = Column(Float)
    volume = Column(Integer)
