from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.util.langhelpers import symbol

# from src.crud import crud, stock
from src import crud
from src import domain_models as dm
from src.core import trade
from src.core.utilities import HTTP400
from src.crud.crud_user import user
from src.domain_models import trading_hours
from src.domain_models.trading_hours import trading_hours_manager
from src.domain_models.user_dm import UserDM
from src.models import User
from src.models.after_order import AfterOrder
from src.schemas.response import Response
from src.schemas.transaction import OrderType, TradeType


class Order(ABC):
    order_type: OrderType

    def __init__(self, symbol, qty, user, db, trade_type, is_pending=False):
        self.symbol = symbol
        self.qty = qty
        self.user = user
        self.db = db
        self.trade_type = trade_type
        self.is_pending = is_pending

    @abstractmethod
    def submit(self):
        pass

    # @abstractmethod
    # def try_execute(self):
    #     pass

    @abstractmethod
    def update(self):
        pass

    def execute(self, price):
        dm.Trade.new(
            self.trade_type, symbol=self.symbol, qty=self.qty, price=price, user=self.user, db=self.db
        ).execute()

    @abstractproperty
    def order_type(self):
        return self.__class__.order_type


class LimitOrder(Order):
    order_type = OrderType.LIMIT

    def __init__(self, limit_price, **kwargs):
        super().__init__(**kwargs)
        self.limit_price = limit_price

    def submit(self):
        if self.qty < 0:
            raise HTTP400(f"Cannot {self.trade_type} negative quantity")

        if self.limit_price < 0:
            raise HTTP400("Limit value cannot be negative")

        # If the order can be executed immediately, execute
        if self.try_execute():
            return Response(msg="Order palced and executed successfully")
        else:
            crud.user.create_order(
                db=self.db,
                user_in=user.model,
                trade_type=self.trade_type,
                symbol=self.symbol,
                quantity=self.qty,
                limit=self.limit_price,
            )
            return Response(msg="Order placed successfully")

    def can_execute(self, curr_price):
        trade_type = dm.Trade.subclass(self.trade_type)
        if trade_type.is_buying:
            return curr_price <= self.limit_price
        else:
            return curr_price >= self.limit_price

    def try_execute(self):
        curr_price = trade.get_stock_price(self.symbol)
        if self.can_execute(curr_price):
            print(f"executing limit order {self.symbol}")
            self.execute(curr_price)
            return True
        return False

    @classmethod
    def from_orm(cls, user, db, order):
        return cls(
            limit_price=order.limit,
            symbol=order.symbol,
            qty=order.amount,
            user=user,
            db=db,
            trade_type=TradeType[order.t_type],
        )


class MarketOrder(Order):
    order_type = OrderType.MARKET

    # TODO move timestamp up to the superclass
    def __init__(self, timestamp, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = timestamp

    # TODO refactor submit function so that the logic is abstracted
    def submit(self):
        if self.qty < 0:
            raise HTTP400(f"Cannot {self.trade_type} negative quantity")

        # If the order can be executed immediately, execute
        if self.try_execute():
            return Response(msg="Order placed and executed successfully")
        else:
            crud.user.add_after_order(
                db=self.db,
                user_in=user.model,
                trade_type_in=self.trade_type,
                amount_in=self.qty,
                symbol_in=self.symbol,
                dt_in=self.timestamp,
            )
            return Response(msg="After market order placed")

    def is_trading(self):
        return trading_hours_manager.is_trading(self.get_stock())

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

    def get_stock(self):
        return crud.stock.get_stock_by_symbol(db=self.db, stock_symbol=self.symbol)

    @classmethod
    def from_orm(cls, user, db, order):
        return cls(
            timestamp=order.date_time,
            symbol=order.symbol,
            qty=order.amount,
            user=user,
            db=db,
            trade_type=TradeType[order.t_type],
        )


class PendingOrderExecutor:
    def __init__(self, db: Session):
        self.db = db

    # TODO place db.flush/expire/commit in correct places
    def update(self):
        for user_m in crud.user.get_all_users(db=self.db):
            self.execute_limit_orders(UserDM(user_m, self.db))

    def execute_limit_orders(self, user):
        for order in user.model.limit_orders:
            print(f"found limit order {order.symbol}")

            if LimitOrder.from_orm(user, self.db, order).try_execute():
                crud.user.delete_order(db=self.db, user_in=user.model, identity=order.id)

    def execute_market_orders(self, user):
        for order in user.model.after_orders:
            print(f"found after order {order.symbol}")

            if MarketOrder.from_orm(user, self.db, order).try_execute():
                crud.user.delete_after_order(db=self.db, user_in=user.model, identity=order.id)


class PendingOrder:
    def __init__(self, db: Session):
        self.db = db
        self.users = user.get_all_users(db=db)

    def update(self):
        for investor in self.users:
            self.execute_limit_orders(investor=investor, db=self.db)
            self.execute_after_orders(investor=investor, db=self.db)

    def execute_limit_orders(self, investor: User, db: Session):
        for order in investor.limit_orders:
            print(f"found limit order {order.symbol}")
            curr_price = trade.get_stock_price(order.symbol)
            transaction = None
            if order.t_type == TradeType.BUY and order.price >= curr_price:
                transaction = dm.BuyTrade(
                    symbol=order.symbol, qty=order.amount, price=order.price, db=db, user=dm.UserDM(investor, db)
                )
            elif order.t_type == TradeType.SELL and order.price <= curr_price:
                transaction = dm.SellTrade(
                    symbol=order.symbol, qty=order.amount, price=order.price, db=db, user=dm.UserDM(investor, db)
                )
            elif order.t_type == TradeType.SHORT and order.price <= curr_price:
                transaction = dm.ShortTrade(
                    symbol=order.symbol, qty=order.amount, price=order.price, db=db, user=dm.UserDM(investor, db)
                )
            elif order.t_type == TradeType.COVER and order.price >= curr_price:
                transaction = dm.CoverTrade(
                    symbol=order.symbol, qty=order.amount, price=order.price, db=db, user=dm.UserDM(investor, db)
                )

            if transaction is not None:
                print(f"executing limit order {order.symbol}")
                transaction.execute()
                user.delete_order(db=db, user_in=investor, identity=order.id)

    def execute_after_orders(self, investor: User, db: Session):
        for order in investor.after_orders:
            stock_obj = crud.stock.get_stock_by_symbol(db=db, stock_symbol=order.symbol)
            exchange = trading_hours.trading_hours_manager.get_exchange(stock_obj.exchange)
            if trading_hours.next_open(order.date_time, exchange) < datetime.now():
                stock_data = next((x for x in stock_obj.timeseries if x.date == datetime.date(order.date_time)), None)
                # TODO: check that data exists for date
                # if stock_data is None, cancel the order (error)
                open_price = stock_data.open
                if order.t_type == TradeType.BUY:
                    transaction = dm.BuyTrade(
                        symbol=order.symbol, qty=order.amount, price=open_price, db=db, user=dm.UserDM(investor, db)
                    )
                elif order.t_type == TradeType.SELL:
                    transaction = dm.SellTrade(
                        symbol=order.symbol, qty=order.amount, price=open_price, db=db, user=dm.UserDM(investor, db)
                    )
                elif order.t_type == TradeType.SHORT:
                    transaction = dm.ShortTrade(
                        symbol=order.symbol, qty=order.amount, price=open_price, db=db, user=dm.UserDM(investor, db)
                    )
                else:
                    transaction = dm.CoverTrade(
                        symbol=order.symbol, qty=order.amount, price=open_price, db=db, user=dm.UserDM(investor, db)
                    )

                transaction.execute()
                user.delete_after_order(db=db, user_in=investor, identity=order.id)
