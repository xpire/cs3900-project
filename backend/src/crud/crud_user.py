"""
CRUD operations for user
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session
from src import crud
from src.core.config import env_settings, settings
from src.core.utilities import fail_save, find, log_msg, ret_initial_users
from src.crud.base import CRUDBase
from src.models.net_worth_timeseries import NetWorthTimeSeries
from src.models.notification import Notification
from src.models.position import LongPosition, ShortPosition
from src.models.transaction import Transaction
from src.models.user import User
from src.models.watchlist import WatchList
from src.schemas.response import Fail, Result, return_result
from src.schemas.transaction import TransactionDBcreate
from src.schemas.user import UserCreate


class CRUDUser(CRUDBase[User]):
    """
    Module for user/auth related CRUD operations
    """

    @return_result()
    def fail_if_stock_missing(self, db, symbol, msg, log_level="WARNING") -> Result:
        """Read the title

        Args:
            db (Session): database session
            symbol (str): stock symbol
            msg (str): failure message
            log_level (str, optional): severity level. Defaults to "WARNING".

        Returns:
            Result: Success/Fail
        """
        if not crud.stock.symbol_exists(db=db, symbol=symbol):
            Fail(msg).log(log_level).ok()

    @fail_save
    def get_all_users(self, db: Session) -> List[User]:
        """Gets all users in the database

        Args:
            db (Session): database session

        Returns:
            List[User]: list of all users
        """
        return self.query(db).all()

    @fail_save
    def get_user_by_uid(self, *, db: Session, uid: str) -> Optional[User]:
        """Read the title

        Args:
            db (Session): database session
            uid (str): user ID

        Returns:
            Optional[User]: user with corresponding user ID
        """
        return self.query(db).get(uid)

    @fail_save
    @return_result()
    def add_to_watchlist(self, *, db: Session, user: User, symbol: str) -> Result:
        """Adds a stock to the users watchlist

        Args:
            db (Session): database session
            user (User): user model
            symbol (str): stock symbol

        Returns:
            Result: Success/Fail
        """
        self.fail_if_stock_missing(
            db, symbol, f"Cannot add a non-existent stock to watchlist of User(uid = {user.uid})."
        )

        if find(user.watchlist, symbol=symbol) is not None:
            return Fail(f"Symbol {symbol} already exists in watchlist.")

        user.watchlist.append(WatchList(user_id=user.uid, symbol=symbol))
        self.commit_and_refresh(db, user)

    @fail_save
    @return_result()
    def delete_from_watchlist(self, *, db: Session, user: User, symbol: str) -> Result:
        """Deletes a stock from the users watchlist

        Args:
            db (Session): database session
            user (User): user model
            symbol (str): stock symbol

        Returns:
            Result: Success/Fail
        """
        self.fail_if_stock_missing(
            db, symbol, f"Cannot delete a non-existent stock from watchlist of User(uid = {user.uid})."
        )

        entry = find(user.watchlist, symbol=symbol)
        if entry is None:
            return Fail(f"Cannot delete a stock that is not in watchlist of User(uid = {user.uid}).").log("WARNING")

        user.watchlist.remove(entry)
        self.commit_and_refresh(db, user)

    @fail_save
    @return_result()
    def update_transaction(self, *, t: TransactionDBcreate, db: Session, user: User) -> Result:
        """Updates the database with an executed trade (buy, sell, short, cover)

        Args:
            t (TransactionDBcreate): transaction details to add (longs/shorts)
            db (Session): database session
            user (User): user model

        Returns:
            Result: Success/Fail
        """
        if t.trade_type.is_opening:
            return self.add_transaction(t=t, db=db, user=user)
        else:
            return self.deduct_transaction(t=t, db=db, user=user)

    @fail_save
    @return_result()
    def add_transaction(
        self,
        *,
        t: TransactionDBcreate,
        db: Session,
        user: User,
    ) -> Result:
        """Udpates database with a purchase trade

        Args:
            t (TransactionDBcreate): transaction details
            db (Session): database session
            user (User): user model

        Returns:
            Result: Success/Fail
        """
        is_long = t.trade_type.is_long

        self.fail_if_stock_missing(
            db, t.symbol, f"Cannot add a non-existent stock to the portfolio of User(uid = {user.uid})."
        )

        positions = user.long_positions if is_long else user.short_positions
        pos = find(positions, symbol=t.symbol)

        if pos is None:
            Position = LongPosition if is_long else ShortPosition
            positions.append(Position(user_id=user.uid, symbol=t.symbol, qty=t.qty, avg=t.price))
        else:
            # compute running average
            new_avg = (pos.avg * pos.qty + t.qty * t.price) / (pos.qty + t.qty)
            new_qty = pos.qty + t.qty

            pos.avg, pos.qty = new_avg, new_qty

        self.commit_and_refresh(db, user)

    @fail_save
    @return_result()
    def deduct_transaction(self, *, db: Session, user: User, t: TransactionDBcreate) -> Result:
        """Update database with a sale transaction

        Args:
            db (Session): database session
            user (User): user model
            t (TransactionDBcreate): transaction details

        Returns:
            Result: Success/Fail
        """
        self.fail_if_stock_missing(
            db, t.symbol, f"Cannot deduct a non-existent stock from the portfolio of User(uid = {user.uid})."
        )

        positions = user.long_positions if t.trade_type.is_long else user.short_positions
        pos = find(positions, symbol=t.symbol)

        if pos is None:
            return Fail(f"Cannot deduct a stock that User(uid = {user.uid}) does not own.").log("WARNING")

        new_qty = pos.qty - t.qty
        if new_qty < 0:
            return Fail(f"Deducting more than owned of User(uid = {user.uid}).").log("WARNING")
        elif new_qty == 0:
            positions.remove(pos)
        else:
            pos.qty = new_qty

        self.commit_and_refresh(db, user)

    @fail_save
    @return_result()
    def delete_user_by_email(self, db: Session, *, email: str) -> Result:
        """Read the title

        Args:
            db (Session): database session
            email (str): email address of user

        Returns:
            Result: Success/Fail
        """
        user = self.query(db).filter_by(email=email).first()
        if user is None:
            return Fail(f"User of email {email} does not exist").log("WARNING")

        db.delete(user)
        db.commit()

    @fail_save
    @return_result()
    def reset(self, *, user: User, db: Session) -> Result:
        """Reset the users portfolio, balance, and transaction history

        Args:
            user (User): user model
            db (Session): database session

        Returns:
            Result: Sucess/Fail
        """
        # reset
        user.balance = settings.STARTING_BALANCE
        user.long_positions = []
        user.short_positions = []
        user.transactions = []
        user.net_worth_history = []

        # set new reset time and amount
        user.resets += 1
        user.last_reset = datetime.now()

        self.commit_and_refresh(db, user)

    @fail_save
    @return_result()
    def add_history(
        self,
        *,
        t: TransactionDBcreate,
        is_cancelled: bool = False,
        db: Session,
        user: User,
    ) -> Result:
        """Adds a transaction to the users transaction history

        Args:
            t (TransactionDBcreate): transaction details
            db (Session): database session
            user (User): user model
            is_cancelled (bool, optional): if the transaction was executed or cancelled. Defaults to False.

        Returns:
            Result: Success/Fail
        """
        user.transaction_hist.append(
            Transaction(
                user_id=user.uid,
                symbol=t.symbol,
                qty=t.qty,
                price=t.price,
                timestamp=t.timestamp,
                order_type=t.order_type,
                trade_type=t.trade_type,
                is_cancelled=is_cancelled,
            )
        )
        self.commit_and_refresh(db, user)

    def insert_init_users(self, db: Session):
        """Inserts a batch of inital users into the database (primarily for demo/testing purposes)

        Args:
            db (Session): database session
        """
        log_msg("Inserting initial users...", "INFO")
        users = ret_initial_users(proj_root=str(env_settings.proj_root))
        for user in users:
            if crud.user.get_user_by_uid(db=db, uid=user["uid"]) == None:
                crud.user.create(db=db, obj=UserCreate(**user))
        log_msg("Done...", "INFO")

    @fail_save
    @return_result()
    def add_historical_portfolio(self, *, user: User, db: Session, timestamp: datetime, net_worth: float) -> Result:
        """Adds a snapshot of the users portfolio value to their history (graphing purposes)

        Args:
            user (User): user model
            db (Session): database session
            timestamp (datetime): time of snapshot
            net_worth (float): current worth

        Returns:
            Result: Success/Fail
        """
        user.net_worth_history.append(
            NetWorthTimeSeries(
                user_id=user.uid,
                timestamp=timestamp,
                net_worth=net_worth,
            )
        )

        self.commit_and_refresh(db, user)

    @return_result()
    def add_notification(self, *, msg, user: User, db: Session) -> Result:
        """Adds a notification to the history of the user's past notifications

        Args:
            msg (NotifMsg): notification message to save
            user (User): user model
            db (Session): database session
        Returns:
            Result: Success/Fail
        """
        user.notifications.append(
            Notification(user_id=user.uid, event_type=msg.event_type, title=msg.title, content=msg.content)
        )
        self.commit_and_refresh(db, user)


user = CRUDUser(User)
