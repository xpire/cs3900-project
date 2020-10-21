from sqlalchemy import Column, ForeignKey, Integer, String
from src.db.base_model import BaseModel


# TODO: consider the option of storing this as a JSON list per user
class UnlockedAchievement(BaseModel):
    user_id = Column(String, ForeignKey("user.uid"), index=True, primary_key=True)
    achievement_id = Column(Integer, primary_key=True)
