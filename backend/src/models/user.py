from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship
from src.db.base_model import BaseModel


class User(BaseModel):
    uid = Column(String, unique=True, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    balance = Column(Float, nullable=False)
    level = Column(Integer, nullable=False)
    exp = Column(Float, nullable=False)
    reset = Column(Integer)
    last_reset = Column(DateTime)
    watchlist = relationship("WatchList", backref="user", cascade="save-update, merge, delete, delete-orphan")
    long_positions = relationship("LongPosition", backref="user", cascade="save-update, merge, delete, delete-orphan")
    short_positions = relationship("ShortPosition", backref="user", cascade="save-update, merge, delete, delete-orphan")
    unlocked_achievements = relationship(
        "UnlockedAchievement", backref="user", cascade="save-update, merge, delete, delete-orphan"
    )
    limit_orders = relationship("LimitOrder", backref="user", cascade="save-update, merge, delete, delete-orphan")
    transaction_hist = relationship("Transaction", backref="user", cascade="save-update, merge, delete, delete-orphan")
