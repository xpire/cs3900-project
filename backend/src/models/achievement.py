"""
Database model for achievements
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from src.db.base_model import BaseModel


class UnlockedAchievement(BaseModel):
    user_id = Column(String, ForeignKey("user.uid"), index=True, primary_key=True)
    achievement_id = Column(Integer, primary_key=True)
