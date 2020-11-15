"""
User domain model. Provides functionalities related to the users account.
"""

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
from src.schemas.notification import UnlockableFeatureType
from src.schemas.response import Fail, Result, Success, return_result


class UserDM:
    def __init__(self, user_m, db: Session):
        self.user_m = user_m
        self.db = db

    def add_exp(self, amount: float):
        """Adds exp to the user

        Args:
            amount (float): amount of exp to add
        """
        level_manager.add_exp(self, amount)

    def unlock_achievement(self, achievement_id: int):
        """Unlocks an achievement for the user

        Args:
            achievement_id (int): achievement to unlock
        """
        if achievement_id in self.model.unlocked_achievements:
            log_msg("Achievement is already unlocked by the user", "ERROR")
            return

        self.model.unlocked_achievements.append(UnlockedAchievement(achievement_id=achievement_id))

    @return_result()
    def reset(self) -> Result:
        """Resets the users portfolio, balance and transaction history

        Returns:
            Result: Success/Fail
        """
        if not self.can_reset_portfolio():
            return Fail(f"Failed to reset, you last resetted {self.model.last_reset}.")

        crud.user.reset(user=self.model, db=self.db)

        event_hub.publish(StatUpdateEvent(user=self))
        return Success("Reset successfully.")

    def can_reset_portfolio(self):
        """Checks if the user is eligible to reset their account

        Returns:
            bool: True if eligible
        """
        if not self.model.last_reset:
            return True
        return (datetime.now() - self.model.last_reset).seconds >= settings.RESET_WAIT_PERIOD_SECONDS

    @property
    def exp(self):
        """Gets the exp

        Returns:
            float: amount of exp user has
        """
        return self.model.exp

    @exp.setter
    def exp(self, exp: float):
        """Sets the users exp

        Args:
            exp (float): amount of exp to set
        """
        self.model.exp = exp
        self.save_to_db()

    @property
    def level(self):
        """Gets the users level

        Returns:
            int: the users level
        """
        return self.model.level

    @level.setter
    def level(self, level: int):
        """Sets the users level

        Args:
            level (int): the level to be set
        """
        self.model.level = level
        self.save_to_db()

    @property
    def balance(self):
        """Gets the users balance

        Returns:
            float: users current balance
        """
        return self.model.balance

    @balance.setter
    def balance(self, balance: float):
        """Sets the users balance

        Args:
            balance (float): balance to be set
        """
        self.model.balance = balance
        self.save_to_db()

    @property
    def exp_until_next_level(self):
        """Gets amount of exp until the next level

        Returns:
            float: exp needed
        """
        return level_manager.exp_until_next_level(self)

    @property
    def is_max_level(self):
        """Checks if the user is max level

        Returns:
            bool: True if max level
        """
        return level_manager.is_max_level(self)

    @property
    def unlocked_achievement_ids(self):
        """Returns set of unlocked achievements

        Returns:
            set: set of achievements the user has unlocked
        """
        return set(x.achievement_id for x in self.model.unlocked_achievements)

    @property
    def achievements(self):
        """Gets all acheivements available with information on users progress

        Returns:
            List[UserAchievement]: list of acheivements
        """
        unlocked = self.unlocked_achievement_ids
        return [UserAchievement(**x.dict(), is_unlocked=x.id in unlocked) for x in achievements_list]

    @property
    def uid(self):
        """Gets the users ID

        Returns:
            str: users ID
        """
        return self.model.uid

    @property
    def short_allowance_rate(self):
        """Returns the percentage the user is allowed to short sell

        Returns:
            float: percentage amount allowed for short selling
        """
        if self.level >= feature_unlocker.level_required(UnlockableFeatureType.SHORT_50):
            return 0.5
        elif self.level >= feature_unlocker.level_required(UnlockableFeatureType.SHORT_25):
            return 0.25
        return 0

    @property
    def schema(self):
        """Returns a user schema for endpoints

        Returns:
            UserAPIout: user schema
        """
        return schemas.UserAPIout(
            **schemas.UserDBout.from_orm(self.model).dict(),
            exp_until_next_level=self.exp_until_next_level,
            exp_threshold=level_manager.get_threshold(self),
            is_max_level=self.is_max_level,
        )

    @property
    def model(self):
        """Returns the user model

        Returns:
            models.User: the user model
        """
        return self.user_m

    def save_to_db(self):
        """
        Refeshes the database
        """
        self.db.commit()
        self.db.refresh(self.model)
