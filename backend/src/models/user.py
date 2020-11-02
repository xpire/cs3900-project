from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship
from src.db.base_model import BaseModel

# TODO simplify relationship parameters
# def has(table_name, backref=True):
#     cascade = "save-update, merge, delete, delete-orphan"
#     if backref:
#         return relationship(table_name, cascade=cascade, backref="user")
#     else:
#         return relationship(table_name, cascade=cascade)


class User(BaseModel):
    uid = Column(String, unique=True, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    balance = Column(Float, nullable=False)

    # watchlist
    watchlist = relationship("WatchList", backref="user", cascade="save-update, merge, delete, delete-orphan")

    # portfolio
    positions = relationship("Position", backref="user", cascade="save-update, merge, delete, delete-orphan")
    long_positions = relationship("LongPosition", cascade="save-update, merge, delete, delete-orphan")
    short_positions = relationship("ShortPosition", cascade="save-update, merge, delete, delete-orphan")

    # orders and history
    pending_orders = relationship("PendingOrder", backref="user", cascade="save-update, merge, delete, delete-orphan")
    limit_orders = relationship("LimitOrder", cascade="save-update, merge, delete, delete-orphan")
    after_orders = relationship("AfterOrder", cascade="save-update, merge, delete, delete-orphan")

    transaction_hist = relationship("Transaction", backref="user", cascade="save-update, merge, delete, delete-orphan")

    # game features
    level = Column(Integer, nullable=False)
    exp = Column(Float, nullable=False)
    resets = Column(Integer, nullable=False, default=0)
    last_reset = Column(DateTime, nullable=True)
    unlocked_achievements = relationship(
        "UnlockedAchievement", backref="user", cascade="save-update, merge, delete, delete-orphan"
    )
