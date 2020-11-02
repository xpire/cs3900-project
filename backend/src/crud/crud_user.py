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
from src import crud, models, schemas
from src.core.config import settings
from src.core.utilities import fail_save, find, log_msg
from src.crud.base import CRUDBase
from src.crud.crud_stock import stock
from src.models.long_position import LongPosition
from src.models.short_position import ShortPosition
from src.models.transaction import Transaction
from src.models.user import User
from src.models.watch_list import WatchList
from src.schemas.response import Fail, Result, Success, return_result
from src.schemas.transaction import TradeType
from src.schemas.user import TransactionHistoryCreate, UserCreate, UserUpdate

# TODO config
STARTING_BALANCE = 10000

'''
class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    Module for user/auth related CRUD operations
    """

    def get_all_users(self, db: Session) -> List[User]:
        return db.query(self.model).all()

    def get_user_by_uid(self, *, db: Session, uid: str) -> Optional[User]:
        """
        Return the corresponding user by token.
        """
        return db.query(self.model).filter(self.model.uid == uid).first()  # Field is unique

    @fail_save
    def update_balance(self, *, db: Session, user_in: User, balance_in: float) -> User:
        """
        Only update the balance of the user.
        """
        user_in.balance = balance_in
        db.commit()
        db.refresh(user_in)
        return user_in

    @fail_save
    def add_to_watch_list(self, *, db: Session, user_in: User, symbol_in: str) -> User:
        """
        Add a watchlist to the user_in's watchlist.
        """
        # BUG: adding existing stocks breaks the code, handle it
        if crud.stock.symbol_exists(db=db, symbol=symbol_in):
            requested_watchlist_entry = WatchList(user_id=user_in.uid, symbol=symbol_in)

            user_in.watchlist.append(requested_watchlist_entry)
            db.commit()
            db.refresh(user_in)
            return user_in
        else:
            log_msg(
                f"Adding a non-existent symbol to watchlist of User(uid = {user_in.uid}).",
                "WARNING",
            )
            return user_in

    @fail_save
    def delete_from_watch_list(self, *, db: Session, user_in: User, symbol_in: str) -> User:
        """
        Delete a watchlist for user_in.
        """
        if crud.stock.symbol_exists(db=db, symbol=symbol_in):
            search_result = None
            for entry in user_in.watchlist:
                if entry.symbol == symbol_in:
                    search_result = entry
                    break

            if search_result == None:
                log_msg(
                    f"Deleting a non-existent stock from watchlist of User(uid = {user_in.uid})",
                    "WARNING",
                )
            else:
                user_in.watchlist.remove(search_result)
                db.commit()
                db.refresh(user_in)

            return user_in
        else:
            log_msg(
                f"Deleting a non-existent symbol from watchlist of User(uid = {user_in.uid}).",
                "WARNING",
            )
            return user_in

    @fail_save
    def add_transaction(
        self,
        *,
        db: Session,
        user_in: User,
        is_long: bool,
        symbol_in: str,
        amount_in: int,
        price_in: float,
    ) -> User:
        """
        Add amount and price to portfolio
        """
        if not crud.stock.symbol_exists(db=db, symbol=symbol_in):
            log_msg(
                f"Adding a non-existent symbol on portfolio of User(uid = {user_in.uid}).",
                "WARNING",
            )
            return user_in

        positions = user_in.long_positions if is_long else user_in.short_positions
        pos = next((x for x in positions if x.symbol == symbol_in), None)

        if pos is None:
            Position = LongPosition if is_long else ShortPosition
            positions.append(Position(user_id=user_in.uid, symbol=symbol_in, amount=amount_in, avg=price_in))
        else:
            # running average used here
            new_avg = (pos.avg * pos.amount + amount_in * price_in) / (pos.amount + amount_in)
            new_amount = pos.amount + amount_in

            pos.avg, pos.amount = new_avg, new_amount

        db.commit()
        db.refresh(user_in)
        return user_in

    @fail_save
    def deduct_transaction(self, *, db: Session, user_in: User, is_long: bool, symbol_in: str, amount_in: int) -> User:
        """
        Remove a stock from portfolio (selling). For type specify 'long' or 'short'
        """

        if not crud.stock.symbol_exists(db=db, symbol=symbol_in):
            log_msg(
                f"Adding a non-existent symbol on portfolio of User(uid = {user_in.uid}).",
                "WARNING",
            )
            return user_in

        positions = user_in.long_positions if is_long else user_in.short_positions
        pos = next((x for x in positions if x.symbol == symbol_in), None)

        if pos is None:
            log_msg(
                f"Deducting a non-existent stock of User(uid = {user_in.uid}).",
                "WARNING",
            )
            return user_in

        new_amount = pos.amount - amount_in
        if new_amount < 0:
            log_msg(
                f"Deducting more than owned of User(uid = {user_in.uid}).",
                "WARNING",
            )
        elif new_amount == 0:
            positions.remove(pos) if is_long else positions.remove(pos)
        else:
            pos.amount = new_amount

        db.commit()
        db.refresh(user_in)
        return user_in

    @fail_save
    def delete_user_by_email(self, db: Session, *, email: str) -> bool:
        obj = db.query(self.model).filter(self.model.email == email).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

    def reset_user_portfolio(self, *, user_in: User, db: Session) -> User:

        # Reset portfolio and transaction history
        user_in.long_positions = []
        user_in.short_positions = []
        user_in.transactions = []

        # Set new reset time and amount
        user_in.resets += 1
        user_in.last_reset = datetime.now()

        db.commit()
        db.refresh(user_in)

        return user_in

    @fail_save
    def add_history(
        self,
        *,
        db: Session,
        user_in: User,
        date_time_in: datetime,
        price_in: float,
        trade_type_in: TradeType,
        amount_in: int,
        symbol_in: str,
    ) -> User:
        """
        Add to the historical transaction.
        """
        requested_record = TransactionHistoryCreate(
            date_time=date_time_in,
            user_id=user_in.uid,
            price=price_in,
            action=trade_type_in.name,
            symbol=symbol_in,
            amount=amount_in,
        )
        user_in.transaction_hist.append(Transaction(**requested_record.__dict__))
        db.commit()
        db.refresh(user_in)
        return user_in


user = CRUDUser(User)
'''


class CRUDUser:
    """
    Module for user/auth related CRUD operations
    """

    def __init__(self, model):
        self.model = model

    def query(self, db):
        return db.query(self.model)

    # TODO turn into decorator
    def commit_and_refresh(self, db, user):
        db.commit()
        db.refresh(user)

    def fail_if_stock_missing(self, db, symbol, msg, log_level="WARNING"):
        if not crud.stock.exists(db=db, symbol=symbol):
            Fail(msg).log(log_level).assert_ok()

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
    @return_result
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
    @return_result
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
    @return_result
    def add_transaction(
        self,
        *,
        symbol: str,
        qty: int,
        price: float,
        is_long: bool,
        db: Session,
        user: User,
    ) -> Result:
        """
        Add stock qty to portfolio
        """
        self.fail_if_stock_missing(
            db, symbol, f"Cannot add a non-existent stock to the portfolio of User(uid = {user.uid})."
        )

        positions = user.long_positions if is_long else user.short_positions
        pos = find(positions, symbol=symbol)

        if pos is None:
            Position = LongPosition if is_long else ShortPosition
            positions.append(Position(user_id=user.uid, symbol=symbol, qty=qty, avg=price))
        else:
            # compute running average
            new_avg = (pos.avg * pos.qty + qty * price) / (pos.qty + qty)
            new_qty = pos.qty + qty

            pos.avg, pos.qty = new_avg, new_qty

        self.commit_and_refresh(db, user)

    @fail_save
    @return_result
    def deduct_transaction(self, *, db: Session, user: User, is_long: bool, symbol: str, qty: int) -> Result:
        """
        Deduct stock qty from portfolio
        """
        self.fail_if_stock_missing(
            db, symbol, f"Cannot deduct a non-existent stock from the portfolio of User(uid = {user.uid})."
        )

        positions = user.long_positions if is_long else user.short_positions
        pos = find(positions, symbol=symbol)

        if pos is None:
            return Fail(f"Cannot deduct a stock that User(uid = {user.uid}) does not own.").log("WARNING")

        new_qty = pos.qty - qty
        if new_qty < 0:
            return Fail(f"Deducting more than owned of User(uid = {user.uid}).").log("WARNING")
        elif new_qty == 0:
            positions.remove(pos)
        else:
            pos.qty = new_qty

        self.commit_and_refresh(db, user)

    @fail_save
    @return_result
    def delete_user_by_email(self, db: Session, *, email: str) -> Result:
        user = self.query(db).filter_by(email=email).first()
        if user is None:
            return Fail(f"User of email {email} does not exist").log("WARNING")

        db.delete(user)
        db.commit()

    @fail_save
    @return_result
    def reset(self, *, user: User, db: Session) -> Result:
        """
        Reset portfolio, transaction history, and balance
        """
        # reset
        user.balance = STARTING_BALANCE
        user.long_positions = []
        user.short_positions = []
        user.transactions = []

        # set new reset time and amount
        user.resets += 1
        user.last_reset = datetime.now()

        self.commit_and_refresh(db, user)

    @fail_save
    @return_result
    def add_history(
        self,
        *,
        symbol: str,
        qty: int,
        price: float,
        trade_type: TradeType,
        timestamp: datetime,
        db: Session,
        user: User,
    ) -> Result:
        """
        Add to the historical transaction.
        """
        user.transaction_hist.append(
            Transaction(
                user_id=user.uid,
                symbol=symbol,
                qty=qty,
                price=price,
                trade_type=trade_type.name,
                timestamp=timestamp,
            )
        )
        self.commit_and_refresh(db, user)


user = CRUDUser(User)


'''

    @fail_save
    @return_result
    def make_trade(
        self,
        *,
        symbol: str,
        qty: int,
        price: float,
        is_long: bool,
        db: Session,
        user: User,
    ) -> Result:
        """
        Add/deduct stock qty to [user]'s portfolio
        """
        self.fail_if_stock_missing(
            db, symbol, f"Cannot add a non-existent stock to the portfolio of User(uid = {user.uid})."
        )

        if qty == 0:
            return Fail("Quantity to trade cannot be 0").log("WARNING")

        positions = user.long_positions if is_long else user.short_positions
        pos = find(positions, symbol=symbol)

        if qty > 0:
            self.add_to_position(
                symbol=symbol, qty=qty, price=price, is_long=is_long, pos=pos, positions=positions, user=user
            ).assert_ok()
        else:
            self.deduct_from_position(qty=-qty, pos=pos, positions=positions, user=user).assert_ok()

        self.commit_and_refresh(db, user)

    @return_result
    def add_to_position(
        self,
        *,
        symbol,
        qty,
        price,
        is_long,
        pos,
        positions,
        user: User,
    ) -> Result:
        if pos is None:
            # TODO refactor this code
            Position = LongPosition if is_long else ShortPosition
            positions.append(Position(user_id=user.uid, symbol=symbol, qty=qty, avg=price))

        else:
            # compute running average
            new_avg = (pos.avg * pos.qty + qty * price) / (pos.qty + qty)
            new_qty = pos.qty + qty

            pos.avg, pos.qty = new_avg, new_qty

    @return_result
    def deduct_from_position(self, *, qty, pos, positions, user: User) -> Result:
        if pos is None:
            return Fail(f"Cannot deduct a stock that User(uid = {user.uid}) does not own.").log("WARNING")

        new_qty = pos.qty - qty
        if new_qty < 0:
            return Fail(f"Deducting more than owned of User(uid = {user.uid}).").log("WARNING")
        elif new_qty == 0:
            positions.remove(pos)
        else:
            pos.qty = new_qty
'''
