from sqlalchemy import Column, String, Float

from backend.src.db.base_class import Base


class User(Base):
    uuid = Column(String, unique=True, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    balance = Column(Float, nullable=False)