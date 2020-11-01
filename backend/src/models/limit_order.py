from abc import ABC, abstractclassmethod, abstractproperty

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.db.base_model import BaseModel


class PendingOrder(BaseModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.uid"))
    symbol = Column(String, ForeignKey("stock.symbol"))
    qty = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)  # TODO consider moving this to the superclass
    trade_type = Column(String, nullable=False)  # buy/sell/short/cover
    order_type = Column(String, nullable=False)
    stock = relationship(  # TODO change name to [stock]
        "Stock",
        cascade="save-update, merge",
    )

    __mapper_args__ = {"polymorphic_identity": "pendingorder", "polymorphic_on": order_type}


class LimitOrder(PendingOrder):
    id = Column(Integer, ForeignKey("pendingorder.id"), primary_key=True)
    limit_price = Column(Float, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "LIMIT",  # TODO replace with order type .name
    }


class AfterOrder(PendingOrder):
    id = Column(Integer, ForeignKey("pendingorder.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "MARKET",
    }
