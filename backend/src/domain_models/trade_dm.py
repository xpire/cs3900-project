from abc import ABC, abstractmethod

from src.core import trade
from src.core.utilities import HTTP400
from src.crud import crud_user
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
        self.execute()

    def execute(self):
        if self.qty < 0:
            raise HTTP400("Cannot trade negative quantity")

        total_price = self.price * self.qty
        trade_price = trade.apply_commission(total_price, self.is_buying())
        fee = abs(trade_price - total_price)
        print(fee)
        self.check(total_price, trade_price)
        self.apply_trade(trade_price)
        return Response(msg="success")

    def apply_trade(self, trade_price):
        update_portfolio = crud_user.user.add_transaction if self.is_opening() else crud_user.user.deduct_transaction
        update_portfolio(self.db, self.model, self.is_long(), self.symbol, self.qty, self.price)
        new_balance = self.model.balance + trade_price * (-1 if self.is_buying() else 1)
        crud_user.user.update_balance(self.db, self.model, new_balance)
        # TODO: add to history

    @abstractmethod
    def check(self, total_price, trade_price):
        pass

    @property
    def model(self):
        return self.user.model


class BuyTrade(Trade):
    def __init__(self, **kwargs):
        super.__init__(**kwargs, is_buying=True, is_long=True, is_opening=True, trade_type=TradeType.BUY)

    def check(self, total_price, trade_price):
        if self.model.balance < trade_price:
            raise HTTP400("Insufficient balance")


class SellTrade(Trade):
    def __init__(self, **kwargs):
        super.__init__(**kwargs, is_buying=False, is_long=True, is_opening=False, trade_type=TradeType.SELL)

    def check(self, total_price, trade_price):
        if not trade.check_owned_longs(self.user, self.qty, self.symbol):
            raise HTTP400("Cannot sell more than owned")


class ShortTrade(Trade):
    def __init__(self, **kwargs):
        super.__init__(**kwargs, is_buying=False, is_long=False, is_opening=True, trade_type=TradeType.SHORT)

    def check(self, total_price, trade_price):
        if not trade.check_short_balance(self.user, total_price):
            raise HTTP400("Insufficient short balance")


class CoverTrade(Trade):
    def __init__(self, **kwargs):
        super.__init__(**kwargs, is_buying=True, is_long=False, is_opening=False, trade_type=TradeType.COVER)

    def check(self, total_price, trade_price):
        if not trade.check_owned_shorts(self.user, self.qty, self.symbol):
            raise HTTP400("Cannot cover more than owed")

        if self.model.balance < trade_price:
            raise HTTP400("Insufficient balance")


# if trade_type is TradeType.BUY:
#     crud_user.user.add_transaction(db, user.model, "long", symbol, qty, stock_price)
#     crud_user.user.update_balance(db, user.model, user.model.balance - trade_price)

# elif trade_type is TradeType.SELL:
#     crud_user.user.deduct_transaction(db, user.model, "long", symbol, qty)
#     crud_user.user.update_balance(db, user.model, user.model.balance + trade_price)

# elif trade_type is TradeType.SHORT:
#     crud_user.user.add_transaction(db, user.model, "short", symbol, qty, stock_price)
#     crud_user.user.update_balance(db, user.model, user.model.balance + trade_price)

# elif trade_type is TradeType.COVER:
#     crud_user.user.deduct_transaction(db, user.model, "short", symbol, qty)
#     crud_user.user.update_balance(db, user.model, user.model.balance - trade_price)


# class BuyTrade:
#     def check(self, total_price, trade_price):
#         if self.model.balance < trade_price:
#             raise HTTP400("Insufficient balance")

#     def is_buying(self):
#         return True

#     def is_long(self):
#         return True

#     def is_opening(self):
#         return True


# def execute_trade(symbol, qty, price, db, user: dm.UserDM, trade_type, check):
#     if qty < 0:
#         raise HTTP400("Cannot trade negative quantity")

#     total_price = price * qty
#     trade_price = trade.apply_commission(total_price, trade_type.is_buying())
#     fee = abs(trade_price - total_price)
#     print(fee)

#     check(user, symbol, qty, price, total_price, trade_price)

#     apply_trade(symbol, qty, price, trade_price, trade_type)
#     return Response("success")
