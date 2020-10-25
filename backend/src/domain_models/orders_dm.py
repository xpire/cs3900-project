from fastapi.param_functions import Depends
import src.api.endpoints.stocks as stocks_api
from sqlalchemy.orm import Session
from src.core.utilities import log_msg
from src.crud.crud_user import user
from src.db.base_model import BaseModel
from src.schemas import User, UserInDB
from src import domain_models as dm
from src.core import trade
from src.schemas.transaction import TradeType


class PendingOrder:
    def __init__(self, db: Session):
        self.db = db
        self.users = user.get_all_users(db)

    def update(self, data):
        for investor in self.users:
            self.execute_pending_orders(investor, self.db)

    def execute_pending_orders(investor: User, db: Session):
        for order in investor.limit_orders:
            curr_price = trade.get_stock_price(order.symbol)
            # TODO: update this to use TRADE TYPE
            if order.type == TradeType.BUY and order.price < curr_price:
                transaction = dm.BuyTrade(order.symbol, order.quantity, order.price, db, investor)
                transaction.execute()
