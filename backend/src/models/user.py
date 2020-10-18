from src.db.base_model import BaseModel
from sqlalchemy import Column, String, Float


class User(BaseModel):
    uuid = Column(String, unique=True, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    balance = Column(Float, nullable=False)