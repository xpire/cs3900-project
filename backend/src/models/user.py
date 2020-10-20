from sqlalchemy import Column, Float, Integer, String
from src.db.base_model import BaseModel
from sqlalchemy.orm import relationship


class User(BaseModel):
    uid = Column(String, unique=True, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    balance = Column(Float, nullable=False)
    level = Column(Integer, nullable=False)
    exp = Column(Float, nullable=False)
    watchlist = relationship(
        "WatchList", backref="user", cascade="save-update, merge, delete, delete-orphan"
    )
    portfolios = relationship(
        "Portfolio", backref="user", cascade="save-update, merge, delete, delete-orphan"
    )
