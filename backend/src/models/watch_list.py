from sqlalchemy import Column, ForeignKey, String
from src.db.base_model import BaseModel


class WatchList(BaseModel):
    user_id = Column(String, ForeignKey("user.uid"), primary_key=True)
    symbol = Column(String, ForeignKey("stock.symbol"), primary_key=True)
