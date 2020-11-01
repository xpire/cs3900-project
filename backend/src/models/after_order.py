from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.models.limit_order import PendingOrder


class AfterOrder(PendingOrder):
    id = Column(Integer, ForeignKey("pendingorder.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "MARKET",
    }
