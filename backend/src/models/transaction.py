"""
Database model for users transactions - executed and cancelled
"""

from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from src.db.base_model import BaseModel
from src.schemas.transaction import OrderType, TradeType


class Transaction(BaseModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.uid"))
    symbol = Column(String, ForeignKey("stock.symbol"))
    qty = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    trade_type = Column(Enum(TradeType), nullable=False)
    order_type = Column(Enum(OrderType), nullable=False)
    timestamp = Column(DateTime)
    is_cancelled = Column(Boolean)
    stock = relationship(
        "Stock",
        backref="transactions",
        cascade="save-update, merge",
    )
