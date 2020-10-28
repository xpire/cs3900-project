from sqlalchemy.orm import Session
from sqlalchemy.util.langhelpers import symbol
from src.crud.crud_user import user
from src.schemas import User
from src import domain_models as dm
from src.core import trade
from src.schemas.transaction import TradeType


class PendingOrder:
    def __init__(self, db: Session):
        self.db = db
        self.users = user.get_all_users(db)

    def update(self, data):
        for investor in self.users:
            self.execute_limit_orders(investor, self.db)

    def execute_limit_orders(investor: User, db: Session):
        for order in investor.limit_orders:
            curr_price = trade.get_stock_price(order.symbol)
            if order.type == TradeType.BUY and order.price >= curr_price:
                transaction = dm.BuyTrade(
                    symbol=order.symbol, qty=order.quantity, price=order.price, db=db, user=investor
                )
                transaction.execute()
            elif order.type == TradeType.SELL and order.price <= curr_price:
                transaction = dm.SellTrade(
                    symbol=order.symbol, qty=order.quantity, price=order.price, db=db, user=investor
                )
                transaction.execute()
            elif order.type == TradeType.SHORT and order.price <= curr_price:
                transaction = dm.ShortTrade(
                    symbol=order.symbol, qty=order.quantity, price=order.price, db=db, user=investor
                )
                transaction.execute()
            elif order.type == TradeType.COVER and order.price >= curr_price:
                transaction = dm.CoverTrade(
                    symbol=order.symbol, qty=order.quantity, price=order.price, db=db, user=investor
                )
                transaction.execute()
