from abc import ABC, abstractmethod
from datetime import datetime

from src.core import trade
from src.core.utilities import HTTP400
from src.crud import crud_user
from src.game.event.sub_events import StatUpdateEvent
from src.game.setup.setup import event_hub
from src.schemas.response import Fail, Response, Result, return_result
from src.schemas.transaction import TradeType


class Trade(ABC):
    trade_type: TradeType = None
    is_buying: bool
    is_long: bool
    is_opening: bool

    def __init__(self, symbol, qty, price, db, user):
        self.symbol = symbol
        self.qty = qty
        self.price = price
        self.db = db
        self.user = user

    @return_result()
    def execute(self) -> Result:
        # Assume qty > 0 check done by order_dm.Order
        total_price = self.price * self.qty
        trade_price = trade.apply_commission(total_price, self.is_buying)
        self.check(total_price, trade_price).assert_ok()
        self.apply_trade(trade_price)

        # Add exp equivalent to the amount of commission deducted
        fee = abs(trade_price - total_price)
        self.user.add_exp(fee)

        event_hub.publish(StatUpdateEvent(user=self.user))

    def apply_trade(self, trade_price):
        if self.is_opening:
            crud_user.user.add_transaction(
                db=self.db,
                user_in=self.model,
                is_long=self.is_long,
                symbol_in=self.symbol,
                amount_in=self.qty,
                price_in=self.price,
            )
        else:
            crud_user.user.deduct_transaction(
                db=self.db, user_in=self.model, is_long=self.is_long, symbol_in=self.symbol, amount_in=self.qty
            )
        new_balance = self.model.balance + trade_price * (-1 if self.is_buying else 1)
        crud_user.user.update_balance(db=self.db, user_in=self.model, balance_in=new_balance)
        crud_user.user.add_history(
            db=self.db,
            user_in=self.model,
            date_time_in=datetime.now(),
            price_in=self.price,
            trade_type_in=self.trade_type,
            amount_in=self.qty,
            symbol_in=self.symbol,
        )

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
        return self.__class__.is_buying

    @property
    def is_long(self):
        return self.__class__.is_long

    @property
    def is_opening(self):
        return self.__class__.is_opening

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
        if self.user.level < 5:
            return Fail(f"Insufficient level. Reach level 5 to short sell")

        if not trade.check_short_balance(self.user, total_price):
            if self.user.level < 10:
                return Fail(
                    f"Insufficient short balance. Reach level 10, buy to cover or increase net worth to short more."
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
        if self.user.level < 5:
            return Fail(f"Insufficient level. Reach level 5 to buy-to-cover")

        if not trade.check_owned_shorts(self.user, self.qty, self.symbol):
            return Fail("Cannot cover more than owed")

        if self.model.balance < trade_price:
            return Fail("Insufficient balance")


Trade.register([BuyTrade, SellTrade, ShortTrade, CoverTrade])
