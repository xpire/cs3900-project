from sqlalchemy import Column, String

from backend.src.db.base_class import Base


class Stock(Base):
    symbol = Column(String, primary_key=True, index=True)
    full_name = Column(String, nullable=True)
    exchange = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    currency = Column(String, nullable=True)
    type = Column(String, nullable=True)
