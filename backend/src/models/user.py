from sqlalchemy import Column, String, Float

from backend.src.db.base_model import BaseModel


class User(BaseModel):
    uuid = Column(String, unique=True, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    balance = Column(Float, nullable=False)