from sqlalchemy import Column, Integer, String, ForeignKey, Float
from src.db.base_model import BaseModel
from sqlalchemy.orm import relationship

# Requires compactification
class Portfolio(BaseModel):
    user_id = Column(String, ForeignKey("user.uid"), primary_key=True)
    symbol = Column(String, ForeignKey("stock.symbol"), primary_key=True)
    amount = Column(Integer, nullable=False)
    avg = Column(Float, nullable=False)
    stock = relationship(
        "Stock",
        backref="watchlist",
        cascade="save-update, merge",
    )