from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

from src import crud
from src import domain_models as dm
from src import schemas
from src.core.utilities import find
from src.db.session import SessionThreadLocal
from src.domain_models import trading_hours
from src.game.feature_unlocker.feature_unlocker import feature_unlocker
from src.schemas.notification import UnlockableFeatureType
from src.schemas.response import Fail, Result, Success, return_result
from src.schemas.transaction import OrderType


class ExecutionFailedException(Exception):
    def __init__(self, result, transaction):
        super().__init__()
        self.result = result
        self.transaction = transaction


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

    @return_result()
    def check_submit(self) -> Result:
        """Negative quantity check

        Returns:
            Result: Success/Fail
        """
        if self.qty <= 0:
            return Fail(f"Must {self.trade_type} positive quantity")

    @return_result()
    def submit(self) -> Result:
        """Attempts to execute the order, handling both 'move to pending' and 'failed to execute'

        Returns:
            Result: Success/Fail
        """
        self.check_submit().ok()

        # If the order can be executed immediately, execute
        try:
            if self.try_execute():
                return Success("Order executed successfully")
            else:
                crud.pending_order.create_order(db=self.db, order=self.schema)
                return Success("Order placed successfully")
        except ExecutionFailedException as e:
            result = e.result
            result.msg = f"Submitted order failed to execute: {result.msg}"
            return result

    @return_result()
    def try_execute(self) -> Result:
        """Differentiates between after hours orders and regular

        Returns:
            Result: Success/Fail
        """
        if not self.is_trading():
            return Fail()

        return self._try_execute()

    @abstractmethod
    def _try_execute(self) -> Result:
        pass

    @return_result()
    def execute(self, price) -> Result:
        """Executes a trade given its parameters

        Args:
            price (float): price of the trade

        Raises:
            ExecutionFailedException: Order could not be executed due to an issue on the users side (e.g. not enough money)

        Returns:
            Result: Success/Fail
        """
        trade = dm.Trade.new(
            self.trade_type,
            symbol=self.symbol,
            qty=self.qty,
            price=price,
            order_type=self.order_type,
            user=self.user,
            db=self.db,
        )
        result = trade.execute()
        if not result.success:
            raise ExecutionFailedException(result=result, transaction=trade.transaction_schema)

        return result

    def is_trading(self):
        """Checks if a stocks' exchange is currently open

        Returns:
            bool: True if trading
        """
        return trading_hours.trading_hours_manager.is_trading(self.get_stock())

    def get_stock(self):
        """Gets a Stock object

        Returns:
            Stock: Stock object
        """
        return crud.stock.get_by_symbol(db=self.db, symbol=self.symbol)

    def get_curr_price(self):
        """Gets latest market price of a stock

        Returns:
            float: latest market price
        """
        return dm.get_data_provider().curr_price(self.symbol)

    @abstractproperty
    def order_type(self):
        return self.__class__.order_type

    @classmethod
    def from_orm_kwargs(cls, user, db, order):
        return dict(
            symbol=order.symbol,
            qty=order.qty,
            timestamp=order.timestamp,
            trade_type=order.trade_type,
            user=user,
            db=db,
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

    @return_result()
    def check_submit(self) -> Result:
        """Saftey checks: level requirements are met, set price not negative

        Returns:
            Result: Success/Fail
        """
        level_limit = feature_unlocker.level_required(UnlockableFeatureType.LIMIT_ORDER)
        if self.user.level < level_limit:
            return Fail(f"You must be level {level_limit} or above to make limit orders.")

        super().check_submit().ok()

        if self.limit_price < 0:
            return Fail("Limit value cannot be negative")

    @return_result()
    def _try_execute(self) -> Result:
        curr_price = self.get_curr_price()
        if not self.can_execute(curr_price):
            return Fail()

        print(f"executing limit order {self.symbol}")
        return self.execute(self.limit_price)

    def can_execute(self, curr_price):
        """Checks whether or not the conditions for the limit order have been reached

        Args:
            curr_price (float): current price of the stock

        Returns:
            bool: True if limit price has been reached
        """
        if self.trade_type.is_buying:
            return curr_price <= self.limit_price
        else:
            return curr_price >= self.limit_price

    @classmethod
    def from_orm_kwargs(cls, user, db, order):
        return dict(limit_price=order.limit_price, **super().from_orm_kwargs(user, db, order))

    @property
    def schema(self):
        data = {**super().schema.dict(), "limit_price": self.limit_price}
        return schemas.LimitOrderDBcreate(**data)


class MarketOrder(Order):
    order_type = OrderType.MARKET

    @return_result()
    def _try_execute(self) -> Result:
        if self.is_pending:
            return self.try_execute_pending()
        else:
            return self.execute(self.get_curr_price())

    @return_result()
    def try_execute_pending(self) -> Result:
        """Attempts to execute after market orders placed previously, at the opening price of the stock

        Returns:
            Result: Success/Fail
        """
        stock = self.get_stock()
        exchange = crud.exchange.get_exchange_by_name(stock.exchange)
        open_datetime = trading_hours.next_open(self.timestamp, exchange)
        if datetime.now() < open_datetime:
            return Fail()

        time_series = find(stock.time_series, date=open_datetime.date())
        if time_series is None:
            return Fail(
                f"Cannot execute market order because open price data for stock {stock.symbol} does not exist."
            ).log()

        return self.execute(time_series.open)

    @property
    def schema(self):
        return schemas.MarketOrderDBcreate(**super().schema.dict())


class PendingOrderExecutor:
    def update(self):
        db = SessionThreadLocal()
        for user_m in crud.user.get_all_users(db=db):
            user = dm.UserDM(user_m, db)
            self.execute_pending_orders(user, user_m.limit_orders, LimitOrder)
            self.execute_pending_orders(user, user_m.after_orders, MarketOrder)

    def execute_pending_orders(self, user, pending_orders, order_cls):
        """Loops through currently pending orders, testing whether their execution conditions have been met

        Args:
            user (User): user model
            pending_orders (Orders): database list of penidng orders
            order_cls (PendingOrder): type of pending order
        """
        db = SessionThreadLocal()
        for order_m in pending_orders:
            order = order_cls.from_orm(user, db, order_m)

            try:
                if order.try_execute():
                    crud.pending_order.delete_order(db=db, id=order_m.id)

            except ExecutionFailedException as e:
                e.result.log()
                crud.pending_order.delete_order(db=db, id=order_m.id)
                crud.user.add_history(
                    t=schemas.TransactionDBcreate(**e.transaction.dict()),
                    is_cancelled=True,
                    db=db,
                    user=user.model,
                )
