"""
Schema for Achievements
"""

from typing import Callable

from pydantic import BaseModel as BaseSchema
from src.game.event.event import GameEvent, GameEventType


class AchievementData(BaseSchema):
    id: int
    name: str
    description: str
    exp: float


class Achievement(AchievementData):
    event_type: GameEventType
    can_unlock: Callable[[GameEvent], bool]


class UserAchievement(AchievementData):
    is_unlocked: bool
