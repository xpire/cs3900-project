from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.db.base_model import BaseModel


class LimitOrder(BaseModel):
    user_id = Column(String, ForeignKey("user.uid"), primary_key=True)
    symbol = Column(String, ForeignKey("stock.symbol"), primary_key=True)
    amount = Column(Integer, nullable=False)
    type = Column(String, nullable=False)  # {long, short}_{buy, sell}
    price = Column(Float, nullable=False)
    stock_info = relationship(
        "Stock",
        backref="limitorder",
        cascade="save-update, merge",
    )
