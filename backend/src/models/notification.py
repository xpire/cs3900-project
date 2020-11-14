"""
Database model for keeping track of user notifications
"""

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from src.db.base_model import BaseModel
from src.schemas.notification import NotifEventType


class Notification(BaseModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.uid"))
    event_type = Column(Enum(NotifEventType), nullable=False)
    title = Column(String)
    content = Column(String)
