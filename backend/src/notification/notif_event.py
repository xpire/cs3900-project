from enum import Enum, auto

from pydantic import BaseModel as BaseSchema
from pydantic import Field

"""
class NotifEventType(str, Enum):
    # LEVEL_UP = "LEVEL_UP"
    # ACHIEVEMENT_UNLOCKED = "ACHIEVEMENT_UNLOCKED"
    LEVEL_UP = ()
    ACHIEVEMENT_UNLOCKED = ()

    def __init__(self):
        self.value = self.name
"""


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class NotifEventType(str, AutoName):
    LEVEL_UP = auto()
    ACHIEVEMENT_UNLOCKED = auto()


class NotifEvent(BaseSchema):
    event_type: NotifEventType


class LevelUpEvent(NotifEvent):
    event_type: NotifEventType = Field(NotifEventType.LEVEL_UP, const=NotifEventType.LEVEL_UP)
    new_level: int


# class AchievementEvent(NotifEvent):
#     event_type:NotifEventType = Field(NotifEventType.LEVEL_UP, const=NotifEventType.LEVEL_UP)
#     description:str
