"""
Database model for user information
"""

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship
from src.db.base_model import BaseModel


def has(table_name, backref=True):
    cascade = "save-update, merge, delete, delete-orphan"
    if backref:
        return relationship(table_name, cascade=cascade, backref="user")
    else:
        return relationship(table_name, cascade=cascade)


class User(BaseModel):
    uid = Column(String, unique=True, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    balance = Column(Float, nullable=False)

    # watchlist
    watchlist = has("WatchList")

    # portfolio
    positions = has("Position")
    long_positions = has("LongPosition", backref=False)
    short_positions = has("ShortPosition", backref=False)

    # orders and history
    pending_orders = has("PendingOrder")
    limit_orders = has("LimitOrder", backref=False)
    after_orders = has("AfterOrder", backref=False)

    transaction_hist = has("Transaction")

    # game features
    level = Column(Integer, nullable=False)
    exp = Column(Float, nullable=False)
    resets = Column(Integer, nullable=False, default=0)
    last_reset = Column(DateTime, nullable=True)
    unlocked_achievements = has("UnlockedAchievement")

    # net worth history
    net_worth_history = has("NetWorthTimeSeries")

    # notifications
    notifications = has("Notification")
