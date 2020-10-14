from sqlalchemy import Column, String, Float

from backend.src.db.base_class import Base

class User(Base):
    username = Column(String, primary_key = True, index = True)
    email = Column(String, unique = True, nullable = False)
    balance = Column(Float, nullable = False)
    token = Column(String, unique = True)
    # Watch list will be here soon