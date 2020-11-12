"""
Database model for users portfolio networth timeseries data
"""

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from src.db.base_model import BaseModel


class NetWorthTimeSeries(BaseModel):
    timestamp = Column(DateTime, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.uid"), primary_key=True)
    net_worth = Column(Float)
