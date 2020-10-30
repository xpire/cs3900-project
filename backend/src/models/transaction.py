from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from src.db.base_model import BaseModel


class Transaction(BaseModel):
    date_time = Column(DateTime, primary_key=True)
    user_id = Column(String, ForeignKey("user.uid"), primary_key=True)
    price = Column(Float, nullable=False)
    action = Column(String)  # buy/sell/short/cover
    symbol = Column(String, ForeignKey("stock.symbol"), primary_key=True)
    amount = Column(Integer, nullable=False)
    stock_info = relationship(
        "Stock",
        backref="transactions",
        cascade="save-update, merge",
    )
