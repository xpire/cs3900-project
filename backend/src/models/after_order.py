from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.db.base_model import BaseModel


class AfterOrder(BaseModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.uid"))
    symbol = Column(String, ForeignKey("stock.symbol"))
    amount = Column(Integer, nullable=False)
    t_type = Column(String, nullable=False)  # buy/sell/short/cover
    date_time = Column(DateTime, nullable=False)
    stock_info = relationship(
        "Stock",
        backref="afterorder",
        cascade="save-update, merge",
    )
    [id, user_id, symbol, amount, t_type, date_time]
