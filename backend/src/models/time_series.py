from src.db.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, String, Float, DateTime


class TimeSeries(BaseModel):
    datetime = Column(DateTime, primary_key=True, index=True)
    symbol = Column(String, ForeignKey("stock.symbol"))
    low = Column(Float)
    high = Column(Float)
    open_p = Column(Float)
    close_p = Column(Float)