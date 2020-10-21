from __future__ import annotations  # resolve circular typing depencies (regarding UserDM)

from collections import defaultdict
from typing import Dict

from src.game.achievement import Achievement, AchievementData
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
        # TODO if event.event_type is not in self.groups
        # additional dict is created - not so clean?
        for x in self.groups[event.event_type].values():
            if x.id in event.user.unlocked_achievement_ids:
                continue

            if x.can_unlock(event):
                self.unlock(event.user, x)

    def unlock(self, user: UserDM, achievement: Achievement):
        achievement_data = AchievementData(**achievement.dict())
        achievement_event = AchievementUnlockedEvent(**achievement_data.dict(), user=user)
        notif_hub.publish(achievement_event)
        user.unlock_achievement(achievement.id)
        user.add_exp(achievement.exp)
