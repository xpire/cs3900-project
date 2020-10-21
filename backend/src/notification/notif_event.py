from enum import auto

from pydantic import BaseModel as BaseSchema
from pydantic import Field
from src.game.achievement import AchievementData
from src.util.auto_name_enum import AutoName
from typing_extensions import Literal


# TODO possibly merge with game event, sharing the event hub
class NotifEventType(str, AutoName):
    LEVEL_UP = auto()
    ACHIEVEMENT_UNLOCKED = auto()


class NotifEvent(BaseSchema):
    event_type: NotifEventType


class LevelUpEvent(NotifEvent):
    event_type: NotifEventType = Field(NotifEventType.LEVEL_UP, const=NotifEventType.LEVEL_UP)
    new_level: int


class AchievementUnlockedEvent(NotifEvent, AchievementData):
    event_type: NotifEventType = Field(NotifEventType.ACHIEVEMENT_UNLOCKED, const=NotifEventType.ACHIEVEMENT_UNLOCKED)
