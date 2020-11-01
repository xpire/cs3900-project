from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.db.base_model import BaseModel
from src.schemas.transaction import OrderType


class PendingOrder(BaseModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.uid"))
    symbol = Column(String, ForeignKey("stock.symbol"))
    qty = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    trade_type = Column(String, nullable=False)  # buy/sell/short/cover
    order_type = Column(String, nullable=False)  # limit/market
    stock = relationship(
        "Stock",
        cascade="save-update, merge",
    )

    __mapper_args__ = {"polymorphic_identity": "pendingorder", "polymorphic_on": order_type}

    # TODO see if this is possible
    # @classmethod
    # def register(cls, subclasses):
    #     cls.type_to_cls = {subclass.order_type: subclass for subclass in subclasses}

    @classmethod
    def register(cls, type_to_cls):
        cls.type_to_cls = type_to_cls

    @classmethod
    def new(cls, order_type, **kwargs):
        return cls.subclass(order_type)(**kwargs)

    @classmethod
    def subclass(cls, order_type):
        return cls.type_to_cls[order_type]


class LimitOrder(PendingOrder):
    id = Column(Integer, ForeignKey("pendingorder.id"), primary_key=True)
    limit_price = Column(Float, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": OrderType.LIMIT.name,
    }


class AfterOrder(PendingOrder):
    id = Column(Integer, ForeignKey("pendingorder.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": OrderType.MARKET.name,
    }


PendingOrder.register({OrderType.LIMIT: LimitOrder, OrderType.MARKET: AfterOrder})
