"""
Database model for pending orders - limit and after market
"""

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.db.base_model import BaseModel
from src.schemas.transaction import OrderType, TradeType


class PendingOrder(BaseModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.uid"))
    symbol = Column(String, ForeignKey("stock.symbol"))
    qty = Column(Integer, nullable=False)
    limit_price = Column(Float, nullable=True)
    timestamp = Column(DateTime, nullable=False)
    trade_type = Column(Enum(TradeType), nullable=False)
    order_type = Column(Enum(OrderType), nullable=False)
    stock = relationship(
        "Stock",
        cascade="save-update, merge",
    )

    __mapper_args__ = {"polymorphic_identity": "pendingorder", "polymorphic_on": order_type}

    @classmethod
    def register(cls, type_to_cls):
        cls.type_to_cls = type_to_cls

    @classmethod
    def subclass(cls, order_type):
        return cls.type_to_cls[order_type]


class LimitOrder(PendingOrder):
    id = Column(Integer, ForeignKey("pendingorder.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": OrderType.LIMIT.name,
    }


class AfterOrder(PendingOrder):
    id = Column(Integer, ForeignKey("pendingorder.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": OrderType.MARKET.name,
    }


PendingOrder.register({OrderType.LIMIT: LimitOrder, OrderType.MARKET: AfterOrder})
