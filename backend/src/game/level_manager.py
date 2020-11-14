from __future__ import annotations  # resolve circular typing depencies (regarding UserDM)

from typing import List, Optional

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
        """Adds experience to the user

        Args:
            user (UserDM): user domain model
            amount (float): amount of exp to add
        """
        user.exp += amount

        while user.level < self.max_level and self.exp_until_next_level(user) <= 0:
            user.exp -= self.get_threshold(user)
            user.level += 1

            self.notif_hub.publish(LevelUpNotifEvent(user=user, new_level=user.level))
            self.event_hub.publish(LevelUpGameEvent(user=user, new_level=user.level))

    def is_max_level(self, user) -> bool:
        """Returns whether the user is max level

        Args:
            user (UserDM): user domain model

        Returns:
            bool: True if max level
        """
        return user.level == self.max_level

    def exp_until_next_level(self, user):
        """Returns amount of exp required to level up

        Args:
            user (UserDM): user domain model

        Returns:
            float: exp until next level
        """
        if self.is_max_level(user):
            return None
        else:
            return self.get_threshold(user) - user.exp

    def get_threshold(self, user) -> Optional[float]:
        """returns amount of exp needed to level up (from 0 exp)

        Args:
            user (UserDM): user domain model

        Returns:
            Optional[float]: amount of exp
        """
        if self.is_max_level(user):
            return None
        else:
            return self.thresholds[user.level - 1]

    @property
    def max_level(self) -> int:
        """returns the maximum level attainable

        Returns:
            int: the maximum level
        """
        return len(self.thresholds) + 1
