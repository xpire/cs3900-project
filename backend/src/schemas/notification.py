from enum import auto

from pydantic import BaseModel as BaseSchema
from src.core.utilities import AutoName


class NotifEventType(str, AutoName):
    GENERIC = auto()
    LEVEL_UP = auto()
    ACHIEVEMENT_UNLOCKED = auto()
    FEATURE_UNLOCKED = auto()


class NotifMsg(BaseSchema):
    event_type: NotifEventType
    title: str
    content: str = ""
    msg_type: str = "notif"


class UnlockableFeatureType(str, AutoName):
    LIMIT_ORDER = auto()
    SHORT_25 = auto()
    SHORT_50 = auto()
    VOLUME = auto()
    EMA = auto()
    BB = auto()
