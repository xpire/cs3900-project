# from __future__ import annotations
from pydantic import Field
from src.game.achievement import Achievement, AchievementData
from src.game.achievement_unlocker import AchievementUnlocker
from src.game.event import GameEvent, GameEventType
from src.game.event_hub import EventHub
from typing_extensions import Literal

"""
EVENTS
"""

# TODO replace other const field with this
class LevelUpEvent(GameEvent):
    event_type: GameEventType = Field(GameEventType.LEVEL_UP, const=GameEventType.LEVEL_UP)
    new_level: int


class AchievementUnlockedEvent(GameEvent, AchievementData):
    event_type: GameEventType = Field(GameEventType.ACHIEVEMENT_UNLOCKED, const=GameEventType.ACHIEVEMENT_UNLOCKED)


"""
ACHIEVEMENTS
"""


def ret_has_reached_level_x(x):
    def has_reached_level(e: LevelUpEvent):
        return e.new_level == x

    return has_reached_level


# TODO: convert to enum?
achievements_list = [
    Achievement(
        id=1,
        name="Good start",
        description="Reach level 3",
        exp=10,
        event_type=GameEventType.LEVEL_UP,
        can_unlock=ret_has_reached_level_x(3),
    ),
    Achievement(
        id=2,
        name="Halfway there!",
        description="Reach level 5",
        exp=60,
        event_type=GameEventType.LEVEL_UP,
        can_unlock=ret_has_reached_level_x(5),
    ),
]

achievements = {x.id: x for x in achievements_list}

if len(achievements) != len(achievements_list):
    raise Exception("Duplicate achievements detected.")

"""
OBJECTS
"""
achievement_unlocker = AchievementUnlocker(achievements)

event_hub = EventHub()
event_hub.subscribe(achievement_unlocker)
