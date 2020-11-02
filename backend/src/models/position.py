from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.db.base_model import BaseModel


class Position(BaseModel):
    user_id = Column(String, ForeignKey("user.uid"), primary_key=True)
    symbol = Column(String, ForeignKey("stock.symbol"), primary_key=True)
    qty = Column(Integer, nullable=False)
    avg = Column(Float, nullable=False)
    position_type = Column(String, nullable=False)  # long/short
    stock = relationship(
        "Stock",
        cascade="save-update, merge",
    )

    __mapper_args__ = {"polymorphic_identity": "position", "polymorphic_on": position_type}

    @classmethod
    def register(cls, type_to_cls):
        cls.type_to_cls = type_to_cls

    @classmethod
    def subclass(cls, order_type):
        return cls.type_to_cls[order_type]


class LongPosition(Position):
    id = Column(Integer, ForeignKey("position.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "LONG",
    }


class ShortPosition(Position):
    id = Column(Integer, ForeignKey("position.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "SHORT",
    }


Position.register({"LONG": LongPosition, "SHORT": ShortPosition})
