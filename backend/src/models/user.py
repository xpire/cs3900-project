from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship
from src.db.base_model import BaseModel


class User(BaseModel):
    uid = Column(String, unique=True, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    balance = Column(Float, nullable=False)
    level = Column(Integer, nullable=False)
    exp = Column(Float, nullable=False)
    watchlist = relationship("WatchList", backref="user", cascade="save-update, merge, delete, delete-orphan")
    portfolios = relationship("Portfolio", backref="user", cascade="save-update, merge, delete, delete-orphan")
    unlocked_achievements = relationship(
        "UnlockedAchievement", backref="user", cascade="save-update, merge, delete, delete-orphan"
    )
