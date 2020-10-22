from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.db.base_model import BaseModel


# Requires compactification
class Portfolio(BaseModel):
    user_id = Column(String, ForeignKey("user.uid"), primary_key=True)
    symbol = Column(String, ForeignKey("stock.symbol"), primary_key=True)
    amount = Column(Integer, nullable=False)
    avg = Column(Float, nullable=False)
    stock_info = relationship(
        "Stock",
        backref="portfolio",
        cascade="save-update, merge",
    )
