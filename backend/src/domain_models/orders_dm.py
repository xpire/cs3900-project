from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.util.langhelpers import symbol
from src import domain_models as dm
from src.core import trade
from src.crud import stock
from src.crud.crud_user import user
from src.domain_models import trading_hours
from src.models import User
from src.schemas.transaction import OrderType, TradeType


class Order(ABC):
    order_type: OrderType

    def __init__(self, symbol, qty, db, user, trade_type):
        self.symbol = symbol
        self.qty = qty
        self.db = db
        self.user = user
        self.trade_type = trade_type

    @abstractmethod
    def submit(self):
        pass

    @abstractmethod
    def try_execute(self):
        pass

    def execute(self, price):
        dm.Trade.new(
            self.trade_type, symbol=self.symbol, qty=self.qty, price=price, db=self.db, user=self.user
        ).execute()

    @abstractproperty
    def order_type(self):
        return self.__class__.order_type


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
            stock_obj = stock.get_stock_by_symbol(db=db, stock_symbol=order.symbol)
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
