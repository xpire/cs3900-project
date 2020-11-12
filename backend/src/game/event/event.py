"""
Enums for game events
"""

from enum import auto
from typing import Any

from pydantic import BaseModel as BaseSchema
from src.core.utilities import AutoName


class GameEventType(str, AutoName):
    TRANSACTION = auto()  # when transactions are executed
    LEVEL_UP = auto()  # when levelling up
    STAT_UPDATE = auto()  # after statistics have been computed
    ACHIEVEMENT_UNLOCKED = auto()


class GameEvent(BaseSchema):
    event_type: GameEventType
    user: Any  # UserDM
