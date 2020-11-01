from abc import ABC, abstractclassmethod, abstractproperty

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.db.base_model import BaseModel


class PendingOrder(BaseModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.uid"))
    symbol = Column(String, ForeignKey("stock.symbol"))
    amount = Column(Integer, nullable=False)
    t_type = Column(String, nullable=False)  # buy/sell/short/cover
    price = Column(Float, nullable=False)
    # stock_info = relationship( #TODO change name to [stock]
    #     "Stock",
    #     backref=stock_backref() #TODO change the names?
    #     cascade="save-update, merge",
    # )

    order_type = Column(String, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "pendingorder", "polymorphic_on": order_type}


class LimitOrder(PendingOrder):
    id = Column(Integer, ForeignKey("pendingorder.id"), primary_key=True)
    stock_info = relationship(
        "Stock",
        backref="limitorder",
        cascade="save-update, merge",
    )

    __mapper_args__ = {
        "polymorphic_identity": "LIMIT",
    }
