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
from src.schemas.response import Response
from src.schemas.transaction import OrderType, TradeType


class Order(ABC):
    order_type: OrderType = None

    def __init__(self, symbol, qty, user, db, trade_type, timestamp, is_pending=False):
        self.symbol = symbol
        self.qty = qty
        self.user = user
        self.db = db
        self.trade_type = trade_type
        self.timestamp = timestamp
        self.is_pending = is_pending

    def check_submit(self):
        if self.qty < 0:
            raise HTTP400(f"Cannot {self.trade_type} negative quantity")

    def submit(self):
        self.check_submit()

        # If the order can be executed immediately, execute
        if self.try_execute():
            return Response(msg="Order executed successfully")
        else:
            crud.pending_order.create_order(db=self.db, order=self.schema)
            return Response(msg="Order placed successfully")

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
        return schemas.PendingOrder(
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

    def check_submit(self):
        self.super().check_submit()
        if self.limit_price < 0:
            raise HTTP400("Limit value cannot be negative")

    def try_execute(self):
        curr_price = trade.get_stock_price(self.symbol)
        if self.can_execute(curr_price):
            print(f"executing limit order {self.symbol}")
            self.execute(curr_price)
            return True
        return False

    def can_execute(self, curr_price):
        trade_type = dm.Trade.subclass(self.trade_type)
        if trade_type.is_buying:
            return curr_price <= self.limit_price
        else:
            return curr_price >= self.limit_price

    @classmethod
    def from_orm_kwargs(cls, user, db, order):
        return dict(limit_price=order.price, **cls.super(cls, cls).from_orm_kwargs(user, db, order))

    @property
    def schema(self):
        return schemas.LimitOrder(
            **self.super().schema.dict(),
            limit_price=self.limit_price,
        )


class MarketOrder(Order):
    order_type = OrderType.MARKET

    def try_execute(self):
        if self.is_pending:
            return self.try_execute_pending()
        else:
            if self.is_trading():
                self.execute(trade.get_stock_price(self.symbol))
                return True
            return False

    def try_execute_pending(self):
        stock = self.get_stock()
        exchange = crud.exchange.get_exchange_by_name(stock.exchange)
        open_datetime = trading_hours.next_open(self.timestamp, exchange)
        if datetime.now() < open_datetime:
            return False

        open_price = next((x.open for x in stock.timeseries if x.date == open_datetime.date()), None)
        # TODO: check that data exists for date
        # if stock is None, cancel the order (error)

        self.execute(open_price)
        return True

    def is_trading(self):
        return trading_hours_manager.is_trading(self.get_stock())

    def get_stock(self):
        return crud.stock.get_stock_by_symbol(db=self.db, stock_symbol=self.symbol)

    @property
    def schema(self):
        return schemas.MarketOrder(**self.super().schema.dict())


class PendingOrderExecutor:
    def __init__(self, db: Session):
        self.db = db

    # TODO place db.flush/expire/commit in correct places
    def update(self):
        for user_m in crud.user.get_all_users(db=self.db):
            self.execute_limit_orders(dm.UserDM(user_m, self.db))

    def execute_limit_orders(self, user):
        self.execute_pending_orders(user, user.model.limit_orders, LimitOrder)

    def execute_market_orders(self, user):
        self.execute_pending_orders(user, user.model.limit_orders, MarketOrder)

    def execute_pending_orders(self, user, pending_orders, order_cls):
        for order in pending_orders:
            if order_cls.from_orm(user, self.db, order).try_execute():
                crud.pending_order.delete_order(db=self.db, id=order.id)
