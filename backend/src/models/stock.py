"""
Database model for each stocks information
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.db.base_model import BaseModel


class Stock(BaseModel):
    symbol = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    exchange = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    currency = Column(String, nullable=True)
    type = Column(String, nullable=True)
    time_series = relationship(
        "TimeSeries",
        backref="stock",
        cascade="save-update, merge",
        lazy="dynamic",
        order_by="TimeSeries.date",
    )
