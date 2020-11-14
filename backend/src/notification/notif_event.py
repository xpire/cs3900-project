"""
Schemas for different types of notification events
"""

from abc import abstractmethod
from enum import auto
from typing import Any

from pydantic import BaseModel as BaseSchema
from src.core.utilities import Const
from src.game.achievement.achievement import Achievement
from src.schemas.notification import NotifEventType, NotifMsg, UnlockableFeatureType


class NotifEvent(BaseSchema):
    event_type: NotifEventType
    user: Any  # UserDM

    @abstractmethod
    def to_msg(self) -> NotifMsg:
        pass


class GenericEvent(NotifEvent):
    event_type: NotifEventType = Const(NotifEventType.GENERIC)
    msg: str

    def to_msg(self) -> NotifMsg:
        return NotifMsg(event_type=self.event_type, title=self.msg, msg_type="generic")


class LevelUpEvent(NotifEvent):
    event_type: NotifEventType = Const(NotifEventType.LEVEL_UP)
    new_level: int

    def to_msg(self) -> NotifMsg:
        return NotifMsg(event_type=self.event_type, title=f"Reached level {self.new_level}!")


class AchievementUnlockedEvent(NotifEvent):
    event_type: NotifEventType = Const(NotifEventType.ACHIEVEMENT_UNLOCKED)
    achievement: Achievement

    def to_msg(self) -> NotifMsg:
        return NotifMsg(event_type=self.event_type, title=self.achievement.name, content=str(self.achievement.exp))


class FeatureUnlockedEvent(NotifEvent):
    event_type: NotifEventType = Const(NotifEventType.FEATURE_UNLOCKED)
    feature_type: UnlockableFeatureType
    msg: str

    def to_msg(self) -> NotifMsg:
        return NotifMsg(event_type=self.event_type, title=self.msg, content=self.feature_type.name)
