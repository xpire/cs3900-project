from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.db.base_model import BaseModel


class AfterHourOrder(BaseModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.uid"))
    symbol = Column(String, ForeignKey("stock.symbol"))
    amount = Column(Integer, nullable=False)
    t_type = Column(String, nullable=False)  # buy/sell/short/cover
    zstock_info = relationship(
        "Stock",
        backref="limitorder",
        cascade="save-update, merge",
    )


symbol, quantity, trade_type, unique_id, placement_date
