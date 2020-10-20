from sqlalchemy import Column, String
from src.db.base_model import BaseModel
from sqlalchemy.orm import relationship


class Stock(BaseModel):
    symbol = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    exchange = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    currency = Column(String, nullable=True)
    type = Column(String, nullable=True)
    timeseries = relationship(
        "TimeSeries",
        backref="stock",
        cascade="save-update, merge",
        lazy="dynamic",
    )
