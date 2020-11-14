"""
Level up achievements
"""

from src.game.achievement.achievement import Achievement
from src.game.event.event import GameEventType
from src.game.event.sub_events import LevelUpEvent
from src.game.setup.config import MAX_LEVEL


def ret_has_reached_level(level):
    """Checks if the user has reached a certain level

    Args:
        level (int): level to be reached
    """

    def has_reached_level(e: LevelUpEvent):
        return e.new_level == level

    return has_reached_level


achievements = [
    Achievement(
        id=1000,
        name="First level up :D",
        description="Reach level 2",
        exp=0,
        event_type=GameEventType.LEVEL_UP,
        can_unlock=ret_has_reached_level(2),
    ),
    Achievement(
        id=1001,
        name="Halfway there!",
        description="Reach level 5",
        exp=0,
        event_type=GameEventType.LEVEL_UP,
        can_unlock=ret_has_reached_level(5),
    ),
    Achievement(
        id=1002,
        name="!!! MAX LEVEL !!!",
        description=f"Reach level {MAX_LEVEL}",
        exp=0,
        event_type=GameEventType.LEVEL_UP,
        can_unlock=ret_has_reached_level(MAX_LEVEL),
    ),
]
