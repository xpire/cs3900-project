from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from src.db.base_model import BaseModel


class Transaction(BaseModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.uid"))
    symbol = Column(String, ForeignKey("stock.symbol"))
    qty = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    trade_type = Column(String)  # buy/sell/short/cover
    timestamp = Column(DateTime)
    stock = relationship(
        "Stock",
        backref="transactions",
        cascade="save-update, merge",
    )
