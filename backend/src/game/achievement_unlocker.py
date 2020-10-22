from __future__ import annotations  # resolve circular typing depencies (regarding UserDM)

from collections import defaultdict
from typing import Dict, List

from src.game.achievement import Achievement
from src.game.event import GameEvent
from src.game.event_hub import EventObserver
from src.notification import AchievementUnlockedEvent, notif_hub


# TODO optimize handling multiple events in one session?
class AchievementUnlocker(EventObserver):
    def __init__(self, achievements: Dict[Achievement]):

        self.achievements = achievements
        self.groups = defaultdict(dict)

        for id, x in achievements.items():
            self.groups[x.event_type][id] = x

    def update(self, event: GameEvent):

        to_unlock = []
        for x in self.groups[event.event_type].values():
            if x.id not in event.user.unlocked_achievement_ids and x.can_unlock(event):
                to_unlock.append(x)

        self.unlock(event.user, to_unlock)

    def unlock(self, user: UserDM, to_unlock: List[Achievement]):
        exp = 0
        for x in to_unlock:
            achievement_event = AchievementUnlockedEvent(user=user, achievement=x)
            notif_hub.publish(achievement_event)
            exp += x.exp
            user.unlock_achievement(x.id)
        user.add_exp(exp)
