from abc import ABC, abstractmethod
from datetime import datetime

from src import crud
from src.core.config import settings
from src.core.utilities import find
from src.domain_models.account_stat_dm import AccountStat
from src.game.event.sub_events import StatUpdateEvent, TransactionEvent
from src.game.feature_unlocker.feature_unlocker import feature_unlocker
from src.game.setup.setup import event_hub
from src.notification.notif_event import UnlockableFeatureType
from src.schemas.response import Fail, Result, return_result
from src.schemas.transaction import (
    ClosingTransaction,
    OpeningTransaction,
    TradeType,
    Transaction,
    TransactionBase,
    TransactionDBcreate,
)


class Trade(ABC):
    trade_type: TradeType = None
    is_buying: bool
    is_long: bool
    is_opening: bool

    def __init__(self, symbol, qty, price, order_type, db, user):
        self.symbol = symbol
        self.qty = qty
        self.price = price
        self.order_type = order_type
        self.db = db
        self.user = user
        self._transaction_schema = None

    @return_result()
    def execute(self) -> Result:
        """Executes the trade

        Returns:
            Result: Success/Fail
        """
        # Assume qty > 0 check done by order_dm.Order
        total_price = self.price * self.qty
        trade_price = apply_commission(total_price, self.is_buying)
        self.check(total_price, trade_price).ok()

        t = self.transaction_schema
        if self.is_opening:
            event_t = OpeningTransaction(**t.dict())
        else:
            event_t = ClosingTransaction(**t.dict(), **AccountStat(self.user).get_profit_info_for_transaction(t))

        self.apply_trade(trade_price, t)

        # Add exp equivalent to the amount of commission deducted
        fee = abs(trade_price - total_price)
        self.user.add_exp(fee)

        self.dispatch_events(event_t)

    def apply_trade(self, trade_price, t: TransactionBase):
        """Applies an executed trade by updating the relevant databases

        Args:
            trade_price (float): amount trade executed for
            t (TransactionBase): Trade object
        """
        t = TransactionDBcreate(**t.dict())
        crud.user.update_transaction(t=t, db=self.db, user=self.model)
        self.user.balance += trade_price * (-1 if self.is_buying else 1)
        crud.user.add_history(t=t, db=self.db, user=self.model)

    def dispatch_events(self, event_t: Transaction):
        """Publishes that the trade has occured, notifying relevant subscribers

        Args:
            event_t (Transaction): [description]
        """
        event_hub.publish(TransactionEvent(user=self.user, transaction=event_t))
        event_hub.publish(StatUpdateEvent(user=self.user))

    @abstractmethod
    @return_result()
    def check(self, total_price, trade_price) -> Result:
        pass

    @property
    def model(self):
        """Gets the current users model

        Returns:
            User: user model
        """
        return self.user.model

    @property
    def trade_type(self):
        """Gets the current trade type

        Returns:
            TradeType: current trade type
        """
        return self.__class__.trade_type

    @property
    def is_buying(self):
        """Returns whether the trade is purchasing shares

        Returns:
            bool: True if buying
        """
        return self.trade_type.is_buying

    @property
    def is_long(self):
        """Returns whether the trade is for a long position

        Returns:
            bool: True if long position
        """
        return self.trade_type.is_long

    @property
    def is_opening(self):
        """Returns whether the trade is opening a position

        Returns:
            bool: True if opening
        """
        return self.trade_type.is_opening

    @property
    def transaction_schema(self):
        """Returns the transaction schema for current trade

        Returns:
            TransactionBase: transaction schema for current trade
        """
        if self._transaction_schema is None:
            self._transaction_schema = TransactionBase(
                symbol=self.symbol,
                qty=self.qty,
                price=self.price,
                timestamp=datetime.now(),
                order_type=self.order_type,
                trade_type=self.trade_type,
            )
        return self._transaction_schema

    @classmethod
    def register(cls, subclasses):
        cls.type_to_cls = {subclass.trade_type: subclass for subclass in subclasses}

    @classmethod
    def new(cls, trade_type, **kwargs):
        return cls.subclass(trade_type)(**kwargs)

    @classmethod
    def subclass(cls, trade_type):
        return cls.type_to_cls[trade_type]


class BuyTrade(Trade):
    trade_type = TradeType.BUY

    @return_result()
    def check(self, total_price, trade_price) -> Result:
        """Checks if balance is sufficient to purchase

        Args:
            total_price (float): unused
            trade_price (float): amount to be deducted

        Returns:
            Result: Success/Fail
        """
        if self.model.balance < trade_price:
            return Fail("Insufficient balance")


class SellTrade(Trade):
    trade_type = TradeType.SELL

    @return_result()
    def check(self, total_price, trade_price) -> Result:
        """Checks if the user owns enough shares to sell

        Args:
            total_price (float): unused
            trade_price (float): unused

        Returns:
            Result: Success/Fail
        """
        if not check_owned_longs(self.user, self.qty, self.symbol):
            return Fail("Cannot sell more than owned")


class ShortTrade(Trade):
    trade_type = TradeType.SHORT

    @return_result()
    def check(self, total_price, trade_price) -> Result:
        """Checks if the user is high enough level to short sell, and if so, if they have sufficient short balance

        Args:
            total_price (float): amount user is attempting to short sell
            trade_price (float): unused

        Returns:
            Result: Success/Fail
        """
        level_short_25 = feature_unlocker.level_required(UnlockableFeatureType.SHORT_25)
        level_short_50 = feature_unlocker.level_required(UnlockableFeatureType.SHORT_50)

        if self.user.level < level_short_25:
            return Fail(f"Insufficient level. Reach level {level_short_25} to short sell")

        if not check_short_balance(self.user, total_price):
            if self.user.level < level_short_50:
                return Fail(
                    f"Insufficient short balance. Reach level {level_short_50}, buy to cover or increase net worth to short more."
                )
            else:
                return Fail(f"Insufficient short balance. Buy to cover or increase net worth to short more.")


class CoverTrade(Trade):
    trade_type = TradeType.COVER

    @return_result()
    def check(self, total_price, trade_price) -> Result:
        """Checks if the user is allowed to cover, and if so, if they have sufficient shorts owed and sufficient balance

        Args:
            total_price (float): unused
            trade_price (float): total cost to be deducted

        Returns:
            Result: Success/Fail
        """
        level_short_25 = feature_unlocker.level_required(UnlockableFeatureType.SHORT_25)
        if self.user.level < level_short_25:
            return Fail(f"Insufficient level. Reach level {level_short_25} to buy-to-cover")

        if not check_owned_shorts(self.user, self.qty, self.symbol):
            return Fail("Cannot cover more than owed")

        if self.model.balance < trade_price:
            return Fail("Insufficient balance")


def apply_commission(price: float, is_buying: bool = True):
    """Applies relevant commission to each trade (increasing price of purchase, decreasing gains of sales)

    Args:
        price (float): trade price
        is_buying (bool, optional): whether the trade is a purchase. Defaults to True.

    Returns:
        float: final trade price
    """
    rate = 1 + (1 if is_buying else -1) * settings.COMMISSION_RATE
    return price * rate


def check_owned(qty: int, symbol: str, positions):
    """Checks if user owns enough of a stock

    Args:
        qty (int): required quantity
        symbol (str): stock symbol
        positions (Position): long or short

    Returns:
        bool: True if owned quantity is sufficient
    """
    pos = find(positions, symbol=symbol)
    return pos is not None and qty <= pos.qty


def check_owned_longs(user, qty: int, symbol: str):
    """Checks if user has enough long positions in a stock

    Args:
        user (userDM): user domain model
        qty (int): required quantity
        symbol (str): stock symbol

    Returns:
        bool: True if owned enough
    """
    return check_owned(qty, symbol, user.model.long_positions)


def check_owned_shorts(user, qty: int, symbol: str):
    """Checks if user has enough short positions in a stock

    Args:
        user (userDM): user domain model
        qty (int): required quantity
        symbol (str): stock symbol

    Returns:
        bool: True if owned enough
    """
    return check_owned(qty, symbol, user.model.short_positions)


def check_short_balance(user, total_price: float):
    """Checks if the user has sufficient short balance

    Args:
        user (userDM): user domain model
        total_price (float): requied amount

    Returns:
        bool: True if short balance is sufficient
    """
    return total_price <= AccountStat(user).short_balance()


Trade.register([BuyTrade, SellTrade, ShortTrade, CoverTrade])
