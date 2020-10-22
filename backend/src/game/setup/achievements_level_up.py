from src.game.achievement.achievement import Achievement
from src.game.event.event import GameEventType
from src.game.event.sub_events import LevelUpEvent
from src.game.setup.config import MAX_LEVEL


def ret_has_reached_level(level):
    def has_reached_level(e: LevelUpEvent):
        return e.new_level == level

    return has_reached_level


achievements = [
    Achievement(
        id=1,
        name="Good start",
        description="Reach level 3",
        exp=0,
        event_type=GameEventType.LEVEL_UP,
        can_unlock=ret_has_reached_level(3),
    ),
    Achievement(
        id=2,
        name="Halfway there!",
        description="Reach level 5",
        exp=0,
        event_type=GameEventType.LEVEL_UP,
        can_unlock=ret_has_reached_level(5),
    ),
    Achievement(
        id=3,
        name="Max Level!",
        description=f"Reach level {MAX_LEVEL}",
        exp=0,
        event_type=GameEventType.LEVEL_UP,
        can_unlock=ret_has_reached_level(MAX_LEVEL),
    ),
]
