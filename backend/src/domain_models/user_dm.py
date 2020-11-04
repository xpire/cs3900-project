from datetime import datetime

from sqlalchemy.orm import Session
from src import crud, schemas
from src.core.config import settings
from src.core.utilities import log_msg
from src.game.achievement.achievement import UserAchievement
from src.game.event.sub_events import StatUpdateEvent
from src.game.feature_unlocker.feature_unlocker import feature_unlocker
from src.game.setup.setup import achievements_list, event_hub, level_manager
from src.models import UnlockedAchievement
from src.notification.notif_event import UnlockableFeatureType
from src.schemas.response import Fail, Result, Success, return_result


class UserDM:
    def __init__(self, user_m, db: Session):
        self.user_m = user_m
        self.db = db

    def add_exp(self, amount: float):
        level_manager.add_exp(self, amount)

    def unlock_achievement(self, achievement_id: int):
        if achievement_id in self.model.unlocked_achievements:
            log_msg("Achievement is already unlocked by the user", "ERROR")
            return

        self.model.unlocked_achievements.append(UnlockedAchievement(achievement_id=achievement_id))

    @return_result()
    def reset(self) -> Result:
        if not self.can_reset_portfolio():
            return Fail(f"Failed to reset, you last resetted {self.model.last_reset}.")

        crud.user.reset(user=self.model, db=self.db)

        event_hub.publish(StatUpdateEvent(user=self))
        return Success("Reset successfully.")

    def can_reset_portfolio(self):
        if not self.model.last_reset:
            return True
        return (datetime.now() - self.model.last_reset).seconds >= settings.RESET_WAIT_PERIOD_SECONDS

    @property
    def exp(self):
        return self.model.exp

    @exp.setter
    def exp(self, exp: float):
        self.model.exp = exp
        self.save_to_db()

    @property
    def level(self):
        return self.model.level

    @level.setter
    def level(self, level: int):
        self.model.level = level
        self.save_to_db()

    @property
    def balance(self):
        return self.model.balance

    @balance.setter
    def balance(self, balance: float):
        self.model.balance = balance
        self.save_to_db()

    @property
    def exp_until_next_level(self):
        return level_manager.exp_until_next_level(self)

    @property
    def is_max_level(self):
        return level_manager.is_max_level(self)

    @property
    def unlocked_achievement_ids(self):
        return set(x.achievement_id for x in self.model.unlocked_achievements)

    @property
    def achievements(self):
        unlocked = self.unlocked_achievement_ids
        return [UserAchievement(**x.dict(), is_unlocked=x.id in unlocked) for x in achievements_list]

    @property
    def uid(self):
        return self.model.uid

    @property
    def short_allowance_rate(self):
        if self.level >= feature_unlocker.level_required(UnlockableFeatureType.SHORT_25):
            return 0.25
        elif self.level >= feature_unlocker.level_required(UnlockableFeatureType.SHORT_50):
            return 0.5
        return 0

    @property
    def schema(self):
        return schemas.User(
            **schemas.UserInDB.from_orm(self.model).dict(),
            exp_until_next_level=self.exp_until_next_level,
            is_max_level=self.is_max_level,
        )

    @property
    def model(self):
        return self.user_m

    def save_to_db(self):
        self.db.commit()
        self.db.refresh(self.model)
