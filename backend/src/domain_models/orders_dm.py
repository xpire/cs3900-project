from sqlalchemy.orm import Session
from sqlalchemy.util.langhelpers import symbol
from src.crud.crud_user import user
from src.crud import stock
from src.schemas import User
from src import domain_models as dm
from src.domain_models import trading_hours
from src.core import trade
from src.schemas.transaction import TradeType
from datetime import datetime
import src.api.endpoints.stocks as stocks_api


class PendingOrder:
    def __init__(self, db: Session):
        self.db = db
        self.users = user.get_all_users(db)

    def update(self, data):
        for investor in self.users:
            self.execute_limit_orders(investor=investor, db=self.db)
            self.execute_after_orders(investor=investor, db=self.db)

    def execute_limit_orders(investor: User, db: Session):
        for order in investor.limit_orders:
            curr_price = trade.get_stock_price(order.symbol)
            transaction = None
            if order.type == TradeType.BUY and order.price >= curr_price:
                transaction = dm.BuyTrade(
                    symbol=order.symbol, qty=order.quantity, price=order.price, db=db, user=investor
                )
            elif order.type == TradeType.SELL and order.price <= curr_price:
                transaction = dm.SellTrade(
                    symbol=order.symbol, qty=order.quantity, price=order.price, db=db, user=investor
                )
            elif order.type == TradeType.SHORT and order.price <= curr_price:
                transaction = dm.ShortTrade(
                    symbol=order.symbol, qty=order.quantity, price=order.price, db=db, user=investor
                )
            elif order.type == TradeType.COVER and order.price >= curr_price:
                transaction = dm.CoverTrade(
                    symbol=order.symbol, qty=order.quantity, price=order.price, db=db, user=investor
                )

            if transaction is not None:
                transaction.execute()

    def execute_after_orders(investor: User, db: Session):
        for order in investor.after_orders:
            stock_obj = stock.get_stock_by_symbol(symbol=order.symbol)
            exchange = trading_hours.trading_hours_manager.get_exchange(stock_obj.exchange)
            if trading_hours.next_open(order.date_time, exchange.start) < datetime.now():
                stock_data = next((x for x in stock_obj.timeseries if x.date == datetime.date(order.date_time)), None)
                # TODO: check that data exists for date
                open_price = stock_data.open
                if order.type == TradeType.BUY:
                    transaction = dm.BuyTrade(
                        symbol=order.symbol, qty=order.quantity, price=open_price, db=db, user=investor
                    )
                elif order.type == TradeType.SELL:
                    transaction = dm.SellTrade(
                        symbol=order.symbol, qty=order.quantity, price=open_price, db=db, user=investor
                    )
                elif order.type == TradeType.SHORT:
                    transaction = dm.ShortTrade(
                        symbol=order.symbol, qty=order.quantity, price=open_price, db=db, user=investor
                    )
                else:
                    transaction = dm.CoverTrade(
                        symbol=order.symbol, qty=order.quantity, price=open_price, db=db, user=investor
                    )

                transaction.execute()