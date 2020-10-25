from typing import List

import src.api.endpoints.stocks as stocks_api
from sqlalchemy.orm import Session
from src.core.utilities import log_msg
from src.crud.crud_user import user
from src.db.base_model import BaseModel
from src.game.achievement.achievement import UserAchievement
from src.game.setup.setup import achievements_list, level_manager
from src.models import UnlockedAchievement
from src.schemas import User, UserInDB


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
            # TODO: update this to get daily opening price, rather than prev day closing
            entry["previous_price"] = float(
                stocks_api.latest_close_price_provider.data[position.symbol][1]
            )
            entry["symbol"] = position.symbol
            entry["name"] = position.stock_info.name
            entry["owned"] = position.amount
            entry["average_paid"] = position.avg
            entry["total_paid"] = position.avg * position.amount
            entry["value"] = entry["price"] * position.amount
            entry["profit"] = entry["value"] - entry["total_paid"]
            entry["day_profit"] = entry["price"] - entry["previous_price"]
            entry["day_return"] = entry["day_profit"] / entry["total_paid"]
            entry["total_return"] = entry["profit"] / entry["total_paid"]

            ret.append(entry)

        return ret

    def get_total_opening_values(self, p_type: str):
        """
        Returns total amount paid for long_positions or
        total amount gained for short_positions
        """
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

        value = 0
        for position in portfolio:
            value += position.amount * position.avg

        return value

    def get_total_closing_values(self, p_type: str):
        """
        Returns total current value of long_positions or
        total current cost to cover short_positions
        """
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

        value = 0
        for position in portfolio:
            curr_price = float(
                stocks_api.latest_close_price_provider.data[position.symbol][0]
            )
            value += position.amount * curr_price

        return value

    def get_long_profit(self):
        """
        Returns total profit if all long positions were closed
        """
        return self.get_total_closing_values("long") - self.get_total_opening_values(
            "long"
        )

    def get_short_profit(self):
        """
        Returns total profit if all short positions were closed
        """
        return self.get_total_opening_values("short") - self.get_total_closing_values(
            "short"
        )

    def get_portfolio_profit(self):
        """
        Returns total profit if all positions were closed
        """
        return self.get_long_profit() + self.get_short_profit()

    def get_net_portfolio_value(self):
        """
        Returns total current value of long and short positions combined
        """
        return self.get_total_closing_values("long") - self.get_total_closing_values(
            "short"
        )

    def get_net_value(self):
        """
        Returns total current value of the investor
        """
        return self.get_net_portfolio_value() + self.model.balance

    def get_gross_value(self):
        """
        Available balance + value of longs
        """
        return self.model.balance + self.get_total_closing_values("long")

    def get_short_balance(self):
        """
        Returns amount the investor can still short sell for
        """
        return self.get_gross_value() * 0.25 - self.get_total_opening_values("short")

    def get_long_return(self):
        total_spent = self.get_total_opening_values("long")
        if total_spent == 0:
            return 0

        return self.get_long_profit() / total_spent

    def get_short_return(self):
        total_spent = self.get_total_closing_values("short")
        if total_spent == 0:
            return 0

        return self.get_short_profit() / total_spent

    def get_portfolio_return(self):
        total_spent = self.get_total_opening_values(
            "long"
        ) + self.get_total_closing_values("short")

        if total_spent == 0:
            return 0

        return self.get_portfolio_profit() / total_spent

    def get_daily_profit(self, p_type: str):
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

        profit = 0
        for position in portfolio:
            curr_price = float(
                stocks_api.latest_close_price_provider.data[position.symbol][0]
            )
            opening_price = float(
                stocks_api.latest_close_price_provider.data[position.symbol][1]
            )
            profit += curr_price - opening_price

        return profit if p_type == "long" else -profit

    def get_daily_total_profit(self):
        return self.get_daily_profit("long") + self.get_daily_profit("short")

    def get_daily_long_return(self):
        total_spent = self.get_total_opening_values("long")
        if total_spent == 0:
            return 0

        return self.get_daily_profit("long") / total_spent

    def get_daily_short_return(self):
        total_spent = self.get_total_closing_values("short")
        if total_spent == 0:
            return 0

        return self.get_daily_profit("short") / total_spent

    def get_daily_total_return(self):
        total_spent = self.get_total_opening_values(
            "long"
        ) + self.get_total_closing_values("short")
        if total_spent == 0:
            return 0

        return self.get_daily_total_profit() / total_spent

    def compile_portfolio_stats(self):
        stats = {}
        stats["total_long_value"] = self.get_total_closing_values("long")
        stats["total_short_value"] = self.get_total_closing_values("short")
        stats["total_portfolio_value"] = self.get_net_portfolio_value()
        stats["total_long_profit"] = self.get_long_profit()
        stats["total_short_profit"] = self.get_short_profit()
        stats["total_portfolio_profit"] = self.get_portfolio_profit()
        stats["total_long_return"] = self.get_long_return()
        stats["total_short_return"] = self.get_short_return()
        stats["total_portfolio_return"] = self.get_portfolio_return()
        stats["daily_long_profit"] = self.get_daily_profit("long")
        stats["daily_short_profit"] = self.get_daily_profit("short")
        stats["daily_total_profit"] = self.get_daily_total_profit()
        stats["daily_long_return"] = self.get_daily_long_return()
        stats["daily_short_return"] = self.get_daily_short_return()
        stats["total_daily_return"] = self.get_daily_total_return()
        stats["balance"] = self.model.balance
        stats["short_balance"] = self.get_short_balance()
        stats["total_value"] = self.get_net_value()

        return stats

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

    def check_exists_watchlist(self, symbol: str):
        for entry in self.user.watchlist:
            if entry.symbol == symbol:
                return True
        return False

    def check_order_exists(self, id: int):
        for order in self.user.limit_orders:
            if order.id == id:
                return True

        return False
