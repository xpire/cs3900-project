from __future__ import annotations  # resolve circular typing depencies

from typing import List


class LevelManager:
    def __init__(self, thresholds: List[float]):
        self.thresholds = thresholds

    def add_exp(self, user: UserDM, amount: float):
        user.exp += amount

        # events = []
        while user.level < self.max_level and self.exp_until_next_level(user) <= 0:
            user.exp -= self.get_threshold(user.level)
            user.level += 1
            # events.append(LevelUpEvent(self.user, self.user.level))
        # event_hub.publish_multi(events)

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


level_manager = LevelManager([10, 20, 30, 40, 50, 60, 70, 80, 90])
