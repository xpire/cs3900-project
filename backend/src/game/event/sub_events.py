"""
Created separately to [event.py] to avoid dependency cycles with e.g. Achievement
"""

from src.core.utilities import Const
from src.game.achievement.achievement import Achievement
from src.game.event.event import GameEvent, GameEventType
from src.schemas.transaction import Transaction


class TransactionEvent(GameEvent):
    event_type: GameEventType = Const(GameEventType.TRANSACTION)
    transaction: Transaction


class LevelUpEvent(GameEvent):
    event_type: GameEventType = Const(GameEventType.LEVEL_UP)
    new_level: int


class AchievementUnlockedEvent(GameEvent):
    event_type: GameEventType = Const(GameEventType.ACHIEVEMENT_UNLOCKED)
    achievement: Achievement


class StatUpdateEvent(GameEvent):
    event_type: GameEventType = Const(GameEventType.STAT_UPDATE)
