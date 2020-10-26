from abc import ABC, abstractmethod

from src.core import trade
from src.core.utilities import HTTP400
from src.crud import crud_user
from src.game.event.sub_events import StatUpdateEvent
from src.game.setup.setup import event_hub
from src.schemas.response import Response
from src.schemas.transaction import TradeType


class Trade(ABC):
    def __init__(self, symbol, qty, price, db, user, is_buying, is_long, is_opening, trade_type):
        self.symbol = symbol
        self.qty = qty
        self.price = price
        self.db = db
        self.user = user
        self.is_buying = is_buying
        self.is_long = is_long
        self.is_opening = is_opening
        self.trade_type = trade_type

    def execute(self):
        if self.qty < 0:
            raise HTTP400("Cannot trade negative quantity")

        total_price = self.price * self.qty
        trade_price = trade.apply_commission(total_price, self.is_buying)
        self.check(total_price, trade_price)
        self.apply_trade(trade_price)

        fee = abs(trade_price - total_price)
        self.user.add_exp(fee)

        event_hub.publish(StatUpdateEvent(user=self.user))
        return Response(msg="success")

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

    @abstractmethod
    def check(self, total_price, trade_price):
        pass

    @property
    def model(self):
        return self.user.model


class BuyTrade(Trade):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, is_buying=True, is_long=True, is_opening=True, trade_type=TradeType.BUY)

    def check(self, total_price, trade_price):
        if self.model.balance < trade_price:
            raise HTTP400("Insufficient balance")


class SellTrade(Trade):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, is_buying=False, is_long=True, is_opening=False, trade_type=TradeType.SELL)

    def check(self, total_price, trade_price):
        if not trade.check_owned_longs(self.user, self.qty, self.symbol):
            raise HTTP400("Cannot sell more than owned")


class ShortTrade(Trade):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, is_buying=False, is_long=False, is_opening=True, trade_type=TradeType.SHORT)

    def check(self, total_price, trade_price):
        if self.user.level < 5:
            raise HTTP400(f"Insufficient level. Reach level 5 to short sell")

        if not trade.check_short_balance(self.user, total_price):
            if self.user.level < 10:
                raise HTTP400(
                    f"Insufficient short balance. Reach level 10, buy to cover or increase net worth to short more."
                )
            else:
                raise HTTP400(f"Insufficient short balance. Buy to cover or increase net worth to short more.")


class CoverTrade(Trade):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, is_buying=True, is_long=False, is_opening=False, trade_type=TradeType.COVER)

    def check(self, total_price, trade_price):
        if self.user.level < 5:
            raise HTTP400(f"Insufficient level. Reach level 5 to buy-to-cover")

        if not trade.check_owned_shorts(self.user, self.qty, self.symbol):
            raise HTTP400("Cannot cover more than owed")

        if self.model.balance < trade_price:
            raise HTTP400("Insufficient balance")
