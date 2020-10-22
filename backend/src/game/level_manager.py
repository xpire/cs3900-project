from __future__ import annotations  # resolve circular typing depencies (regarding UserDM)

from typing import List

from src.game.event.event_hub import EventHub
from src.game.event.sub_events import LevelUpEvent as LevelUpGameEvent
from src.notification import LevelUpEvent as LevelUpNotifEvent
from src.notification.notifier import NotificationHub


class LevelManager:
    def __init__(self, thresholds: List[float], event_hub: EventHub, notif_hub: NotificationHub):
        self.event_hub = event_hub
        self.notif_hub = notif_hub
        self.thresholds = thresholds

    def add_exp(self, user: UserDM, amount: float):
        user.exp += amount

        while user.level < self.max_level and self.exp_until_next_level(user) <= 0:
            user.exp -= self.get_threshold(user.level)
            user.level += 1

            self.notif_hub.publish(LevelUpNotifEvent(user=user, new_level=user.level))
            self.event_hub.publish(LevelUpGameEvent(user=user, new_level=user.level))

    def is_max_level(self, user: UserDM) -> bool:
        return user.level == self.max_level

    def exp_until_next_level(self, user):
        if self.is_max_level(user):
            return None
        else:
            return self.get_threshold(user.level) - user.exp

    def get_threshold(self, level: int) -> float:
        return self.thresholds[level - 1]

    @property
    def max_level(self) -> int:
        return len(self.thresholds) + 1
