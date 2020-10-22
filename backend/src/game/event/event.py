from enum import auto
from typing import Any

from pydantic import BaseModel as BaseSchema
from src.util.auto_name_enum import AutoName


class GameEventType(str, AutoName):
    TRANSACTION = auto()  # when transactions are executed
    LEVEL_UP = auto()  # when levelling up
    STATISTICS = auto()  # after statistics have been computed
    # ACTION = auto()  # e.g. read a wiki
    ACHIEVEMENT_UNLOCKED = auto()


class GameEvent(BaseSchema):
    event_type: GameEventType
    user: Any  # UserDM
