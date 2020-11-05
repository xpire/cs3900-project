"""
    File name: crud_user.py
    Author: Peiyu Tang
    Date created: 10/15/2020
    Python Version: 3.7.3
    Purpose: Handles user CRUD operations on database 
"""


from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session
from src import crud
from src.core.config import settings
from src.core.utilities import fail_save, find
from src.crud.base import CRUDBase
from src.models.position import LongPosition, ShortPosition
from src.models.transaction import Transaction
from src.models.user import User
from src.models.watchlist import WatchList
from src.schemas.response import Fail, Result, return_result
from src.schemas.transaction import TradeType, TransactionBase, TransactionDBcreate


class CRUDUser(CRUDBase[User]):
    """
    Module for user/auth related CRUD operations
    """

    @return_result()
    def fail_if_stock_missing(self, db, symbol, msg, log_level="WARNING") -> Result:
        if not crud.stock.symbol_exists(db=db, symbol=symbol):
            Fail(msg).log(log_level).ok()

    @fail_save
    def get_all_users(self, db: Session) -> List[User]:
        return self.query(db).all()

    @fail_save
    def get_user_by_uid(self, *, db: Session, uid: str) -> Optional[User]:
        """
        Return the corresponding user by uid.
        """
        return self.query(db).get(uid)

    @fail_save
    @return_result()
    def add_to_watchlist(self, *, db: Session, user: User, symbol: str) -> Result:
        """
        Add a watchlist to the user's watchlist.
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
        """
        Delete a watchlist for user.
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
        """
        Add stock qty to portfolio
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
        """
        Deduct stock qty from portfolio
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
        user = self.query(db).filter_by(email=email).first()
        if user is None:
            return Fail(f"User of email {email} does not exist").log("WARNING")

        db.delete(user)
        db.commit()

    @fail_save
    @return_result()
    def reset(self, *, user: User, db: Session) -> Result:
        """
        Reset portfolio, transaction history, and balance
        """
        # reset
        user.balance = settings.STARTING_BALANCE
        user.long_positions = []
        user.short_positions = []
        user.transactions = []

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
        """
        Add to the historical transaction.
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


user = CRUDUser(User)
