from sqlalchemy.orm import Session
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
            if order.type == TradeType.BUY and order.price < curr_price:
                transaction = dm.BuyTrade(order.symbol, order.quantity, order.price, db, investor)
                transaction.execute()

    def execute_after_market_orders(investor: User, db: Session):
        pass