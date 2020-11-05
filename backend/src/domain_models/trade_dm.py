from abc import ABC, abstractmethod
from datetime import datetime

from src import crud
from src.core import trade
from src.core.utilities import find
from src.domain_models.account_stat_dm import AccountStat
from src.game import event
from src.game.event.sub_events import StatUpdateEvent, TransactionEvent
from src.game.feature_unlocker.feature_unlocker import feature_unlocker
from src.game.setup.setup import event_hub
from src.notification.notif_event import UnlockableFeatureType
from src.schemas.response import Fail, Result, return_result

# TODO move to schemas .__init__?
from src.schemas.transaction import (
    ClosingTransaction,
    OpeningTransaction,
    TradeType,
    TransactionBase,
    TransactionDBcreate,
)


# TODO move logic from trade.py to here
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
        # Assume qty > 0 check done by order_dm.Order
        total_price = self.price * self.qty
        trade_price = trade.apply_commission(total_price, self.is_buying)
        self.check(total_price, trade_price).ok()

        t = self.transaction_schema
        self.apply_trade(trade_price, t)

        # Add exp equivalent to the amount of commission deducted
        fee = abs(trade_price - total_price)
        self.user.add_exp(fee)

        self.dispatch_events(t)

    def apply_trade(self, trade_price, t: TransactionBase):
        t = TransactionDBcreate(**t.dict())
        crud.user.update_transaction(t=t, db=self.db, user=self.model)
        self.user.balance += trade_price * (-1 if self.is_buying else 1)
        crud.user.add_history(t=t, db=self.db, user=self.model)

    def dispatch_events(self, t: TransactionBase):
        if self.is_opening:
            t = OpeningTransaction(**t.dict())
        else:
            t = ClosingTransaction(**t.dict(), **AccountStat(self.user).get_profit_info_for_transaction(t))

        event_hub.publish(TransactionEvent(user=self.user, transaction=t))
        event_hub.publish(StatUpdateEvent(user=self.user))

    @abstractmethod
    @return_result()
    def check(self, total_price, trade_price) -> Result:
        pass

    @property
    def model(self):
        return self.user.model

    @property
    def trade_type(self):
        return self.__class__.trade_type

    @property
    def is_buying(self):
        return self.trade_type.is_buying

    @property
    def is_long(self):
        return self.trade_type.is_long

    @property
    def is_opening(self):
        return self.trade_type.is_opening

    @property
    def transaction_schema(self):
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
    is_buying = True
    is_long = True
    is_opening = True

    @return_result()
    def check(self, total_price, trade_price) -> Result:
        if self.model.balance < trade_price:
            return Fail("Insufficient balance")


class SellTrade(Trade):
    trade_type = TradeType.SELL
    is_buying = False
    is_long = True
    is_opening = False

    @return_result()
    def check(self, total_price, trade_price) -> Result:
        if not trade.check_owned_longs(self.user, self.qty, self.symbol):
            return Fail("Cannot sell more than owned")


class ShortTrade(Trade):
    trade_type = TradeType.SHORT
    is_buying = False
    is_long = False
    is_opening = True

    @return_result()
    def check(self, total_price, trade_price) -> Result:
        level_short_25 = feature_unlocker.level_required(UnlockableFeatureType.SHORT_25)
        level_short_50 = feature_unlocker.level_required(UnlockableFeatureType.SHORT_50)

        if self.user.level < level_short_25:
            return Fail(f"Insufficient level. Reach level {level_short_25} to short sell")

        if not trade.check_short_balance(self.user, total_price):
            if self.user.level < level_short_50:
                return Fail(
                    f"Insufficient short balance. Reach level {level_short_50}, buy to cover or increase net worth to short more."
                )
            else:
                return Fail(f"Insufficient short balance. Buy to cover or increase net worth to short more.")


class CoverTrade(Trade):
    trade_type = TradeType.COVER
    is_buying = True
    is_long = False
    is_opening = False

    @return_result()
    def check(self, total_price, trade_price) -> Result:
        level_short_25 = feature_unlocker.level_required(UnlockableFeatureType.SHORT_25)
        if self.user.level < level_short_25:
            return Fail(f"Insufficient level. Reach level {level_short_25} to buy-to-cover")

        if not trade.check_owned_shorts(self.user, self.qty, self.symbol):
            return Fail("Cannot cover more than owed")

        if self.model.balance < trade_price:
            return Fail("Insufficient balance")


Trade.register([BuyTrade, SellTrade, ShortTrade, CoverTrade])
