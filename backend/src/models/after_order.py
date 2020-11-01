from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.models.limit_order import PendingOrder


class AfterOrder(PendingOrder):
    id = Column(Integer, ForeignKey("pendingorder.id"), primary_key=True)
    date_time = Column(DateTime, nullable=False)  # TODO consider moving this to the superclass
    stock_info = relationship(
        "Stock",
        backref="afterorder",  # TODO change these names, just remove
        cascade="save-update, merge",
    )

    __mapper_args__ = {
        "polymorphic_identity": "MARKET",
    }
