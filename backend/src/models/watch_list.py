from sqlalchemy import Column, ForeignKey, String
from src.db.base_model import BaseModel
from sqlalchemy.orm import relationship


class WatchList(BaseModel):
    user_id = Column(String, ForeignKey("user.uid"), primary_key=True)
    symbol = Column(String, ForeignKey("stock.symbol"), primary_key=True)
    stock_info = relationship(
        "Stock",
        backref="watchlist",
        cascade="save-update, merge",
    )
