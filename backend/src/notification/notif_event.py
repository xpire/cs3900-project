from enum import auto
from typing import Any

from pydantic import BaseModel as BaseSchema
from pydantic import Field
from src.game.achievement import AchievementData
from src.util.auto_name_enum import AutoName
from src.util.extended_types import Const


# TODO possibly merge with game event, sharing the event hub
class NotifEventType(str, AutoName):
    LEVEL_UP = auto()
    ACHIEVEMENT_UNLOCKED = auto()


class NotifEvent(BaseSchema):
    event_type: NotifEventType
    user: Any  # UserDM


class LevelUpEvent(NotifEvent):
    event_type: NotifEventType = Const(NotifEventType.LEVEL_UP)
    new_level: int


class AchievementUnlockedEvent(NotifEvent, AchievementData):
    event_type: NotifEventType = Const(NotifEventType.ACHIEVEMENT_UNLOCKED)
