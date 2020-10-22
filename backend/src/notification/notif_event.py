from abc import abstractmethod
from enum import auto
from typing import Any

from pydantic import BaseModel as BaseSchema
from pydantic import Field
from src.game.achievement import Achievement
from src.util.auto_name_enum import AutoName
from src.util.extended_types import Const


# TODO possibly merge with game event, sharing the event hub
class NotifEventType(str, AutoName):
    LEVEL_UP = auto()
    ACHIEVEMENT_UNLOCKED = auto()


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
