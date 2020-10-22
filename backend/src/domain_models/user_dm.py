from typing import List

from sqlalchemy.orm import Session
from src.core.utilities import log_msg
from src.crud.crud_user import user
from src.db.base_model import BaseModel
from src.game.achievement.achievement import UserAchievement
from src.game.setup.setup import achievements_list, level_manager
from src.models import UnlockedAchievement
from src.schemas import User, UserInDB

import src.api.endpoints.stocks as stocks_api

# TODO move this and relevant imports somewhere
def update(model: BaseModel, db: Session):
    db.add(model)
    db.commit()
    db.refresh(model)


# TODO save_to_db can be done at the end
class UserDM:
    def __init__(self, user: User, db: Session):
        self.user = user
        self.db = db

    def add_exp(self, amount: float):
        level_manager.add_exp(self, amount)
        self.save_to_db()

    def unlock_achievement(self, achievement_id: int):
        if achievement_id in self.user.unlocked_achievements:
            log_msg("Achievement is already unlocked by the user", "ERROR")
            return

        self.user.unlocked_achievements.append(
            UnlockedAchievement(achievement_id=achievement_id)
        )
        self.save_to_db()

    def save_to_db(self):
        update(self.user, self.db)

    @property
    def exp(self):
        return self.user.exp

    @exp.setter
    def exp(self, exp: float):
        self.user.exp = exp

    @property
    def level(self):
        return self.user.level

    @level.setter
    def level(self, level: int):
        self.user.level = level

    @property
    def exp_until_next_level(self):
        return level_manager.exp_until_next_level(self)

    @property
    def is_max_level(self):
        return level_manager.is_max_level(self)

    @property
    def unlocked_achievement_ids(self):
        return set(x.achievement_id for x in self.user.unlocked_achievements)

    @property
    def achievements(self):
        unlocked = self.unlocked_achievement_ids
        return [
            UserAchievement(**x.dict(), is_unlocked=x.id in unlocked)
            for x in achievements_list
        ]

    @property
    def uid(self):
        return self.user.uid

    @property
    def schema(self):
        return User(
            **UserInDB.from_orm(self.user).dict(),
            exp_until_next_level=self.exp_until_next_level,
            is_max_level=self.is_max_level
        )

    @property
    def model(self):
        return self.user

    def get_positions(self, p_type: str):
        if p_type != "long" and p_type != "short":
            log_msg(
                "No such position. allowed are 'long' or'short'.",
                "ERROR",
            )
            return

        portfolio = (
            self.model.long_positions
            if p_type == "long"
            else self.model.short_positions
        )

        ret = []

        for position in portfolio:
            entry = {}
            entry["price"] = float(
                stocks_api.latest_close_price_provider.data[position.symbol][0]
            )
            entry["previous_price"] = float(
                stocks_api.latest_close_price_provider.data[position.symbol][1]
            )
            entry["symbol"] = position.symbol
            entry["name"] = position.stock_info.name
            entry["owned"] = position.amount
            entry["average_paid"] = position.avg
            entry["total_paid"] = position.avg * position.amount
            entry["value"] = entry["price"] * position.amount
            entry["gain"] = entry["value"] - entry["total_paid"]
            entry["day_gain"] = entry["price"] - entry["previous_price"]
            entry["return"] = entry["gain"] / entry["total_paid"]

            ret.append(entry)

        return ret

    def watchlist_create(self, wl_sys: str):
        self.user = user.add_to_watch_list(
            db=self.db, user_in=self.user, w_symbol=wl_sys
        )
        return self.user

    def watchlist_delete(self, wl_sys: str):
        self.user = user.delete_from_watch_list(
            db=self.db, user_in=self.user, w_symbol=wl_sys
        )
        return self.user

    def get_gross_value(self):
        """
        Available balance + value of longs
        """
        value = self.user.balance
        for position in self.user.long_positions:
            value += position.amount * position.avg

        return value

    def get_shorts_owing(self):
        """
        Returns amount user has currently short sold for
        """
        value = 0
        for position in self.user.short_positions:
            value += position.amount * position.avg

        return value

    def get_short_balance(self):
        """
        Returns amount the investor can still short sell for
        """
        return self.get_gross_value() * 0.25 - self.get_shorts_owing()
