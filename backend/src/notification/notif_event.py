from abc import abstractmethod
from enum import auto
from typing import Any

from pydantic import BaseModel as BaseSchema
from src.game.achievement.achievement import Achievement
from src.util.auto_name_enum import AutoName
from src.util.extended_types import Const


class NotifEventType(str, AutoName):
    LEVEL_UP = auto()
    ACHIEVEMENT_UNLOCKED = auto()
    FEATURE_UNLOCKED = auto()


class UnlockableFeatureType(str, AutoName):
    LIMIT_ORDER = auto()
    SHORT_25 = auto()
    SHORT_50 = auto()


class NotifMsg(BaseSchema):
    event_type: NotifEventType
    title: str
    content: str = ""


class NotifEvent(BaseSchema):
    event_type: NotifEventType
    user: Any  # UserDM

    @abstractmethod
    def to_msg(self) -> NotifMsg:
        pass


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
