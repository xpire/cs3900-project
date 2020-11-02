from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

from sqlalchemy.orm import Session
from src import crud
from src import domain_models as dm
from src import schemas
from src.core import trade
from src.core.utilities import HTTP400
from src.domain_models import trading_hours
from src.domain_models.trading_hours import trading_hours_manager
from src.schemas.response import Fail, Response, Success, return_result
from src.schemas.transaction import OrderType, TradeType

# TODO
"""
1. update trade.py
2. update orders.py
3. update others as necessary
4. refactor crud
"""


class Order(ABC):
    order_type: OrderType = None

    def __init__(self, symbol, qty, user, db, trade_type, timestamp=None, is_pending=False):
        self.symbol = symbol
        self.qty = qty
        self.user = user
        self.db = db
        self.trade_type = trade_type
        self.timestamp = datetime.now() if timestamp is None else timestamp
        self.is_pending = is_pending

    @return_result
    def check_submit(self):
        if self.qty < 0:
            return Fail(f"Cannot {self.trade_type} negative quantity")

    @return_result
    def submit(self):
        self.check_submit().check()

        # If the order can be executed immediately, execute
        if self.try_execute():
            return Success("Order executed successfully")
        else:
            crud.pending_order.create_order(db=self.db, order=self.schema)
            return Success("Order placed successfully")

    @abstractmethod
    def try_execute(self):
        pass

    def execute(self, price):
        dm.Trade.new(
            self.trade_type, symbol=self.symbol, qty=self.qty, price=price, user=self.user, db=self.db
        ).execute()

    @abstractproperty
    def order_type(self):
        return self.__class__.order_type

    @classmethod
    def from_orm_kwargs(cls, user, db, order):
        return dict(
            symbol=order.symbol,
            qty=order.qty,
            timestamp=order.timestamp,
            user=user,
            db=db,
            trade_type=TradeType[order.t_type],
            is_pending=True,
        )

    @classmethod
    def from_orm(cls, user, db, order):
        return cls(**cls.from_orm_kwargs(user, db, order))

    @abstractproperty
    def schema(self):
        return schemas.PendingOrderDBcreate(
            user_id=self.user.model.uid,
            symbol=self.symbol,
            qty=self.qty,
            trade_type=self.trade_type,
            order_type=self.__class__.order_type,
            timestamp=self.timestamp,
        )


class LimitOrder(Order):
    order_type = OrderType.LIMIT

    def __init__(self, limit_price, **kwargs):
        super().__init__(**kwargs)
        self.limit_price = limit_price

    @return_result
    def check_submit(self):
        super().check_submit().check()

        if self.limit_price < 0:
            return Fail("Limit value cannot be negative")

    @return_result
    def try_execute(self):
        curr_price = trade.get_stock_price(self.symbol)
        if not self.can_execute(curr_price):
            return Fail()

        print(f"executing limit order {self.symbol}")
        self.execute(curr_price)

    def can_execute(self, curr_price):
        trade_type = dm.Trade.subclass(self.trade_type)
        if trade_type.is_buying:
            return curr_price <= self.limit_price
        else:
            return curr_price >= self.limit_price

    @classmethod
    def from_orm_kwargs(cls, user, db, order):
        return dict(limit_price=order.price, **super().from_orm_kwargs(user, db, order))

    @property
    def schema(self):
        data = {**super().schema.dict(), "limit_price": self.limit_price}
        return schemas.LimitOrderDBcreate(**data)


class MarketOrder(Order):
    order_type = OrderType.MARKET

    def try_execute(self):
        if self.is_pending:
            return self.try_execute_pending()
        else:
            if not self.is_trading():
                return Fail()

            self.execute(trade.get_stock_price(self.symbol))

    @return_result
    def try_execute_pending(self):
        stock = self.get_stock()
        exchange = crud.exchange.get_exchange_by_name(stock.exchange)
        open_datetime = trading_hours.next_open(self.timestamp, exchange)
        if datetime.now() < open_datetime:
            return Fail()

        open_price = next((x.open for x in stock.timeseries if x.date == open_datetime.date()), None)

        if open_price is None:
            return Fail(
                f"Cannot exectue market order because open price data for stock {stock.symbol} does not exist."
            ).log()

        self.execute(open_price)

    def is_trading(self):
        return trading_hours_manager.is_trading(self.get_stock())

    def get_stock(self):
        return crud.stock.get_stock_by_symbol(db=self.db, symbol=self.symbol)

    @property
    def schema(self):
        return schemas.MarketOrderDBcreate(**super().schema.dict())


class PendingOrderExecutor:
    def __init__(self, db: Session):
        self.db = db

    # TODO place db.flush/expire/commit in correct places
    def update(self):
        for user_m in crud.user.get_all_users(db=self.db):
            user = dm.UserDM(user_m, self.db)
            self.execute_pending_orders(user, user_m.limit_orders, LimitOrder)
            self.execute_pending_orders(user, user_m.after_orders, MarketOrder)

    def execute_pending_orders(self, user, pending_orders, order_cls):
        for order in pending_orders:
            if order_cls.from_orm(user, self.db, order).try_execute():
                crud.pending_order.delete_order(db=self.db, id=order.id)
