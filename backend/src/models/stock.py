from src.db.base_model import BaseModel
from sqlalchemy import Column, String


class Stock(BaseModel):
    symbol = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    exchange = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    currency = Column(String, nullable=True)
    type = Column(String, nullable=True)
