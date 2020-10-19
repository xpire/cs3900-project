from sqlalchemy import Column, Float, String
from src.db.base_model import BaseModel


class User(BaseModel):
    uid = Column(String, unique=True, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    balance = Column(Float, nullable=False)
