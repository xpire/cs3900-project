"""
    File name: crud_user.py
    Author: Peiyu Tang
    Date created: 10/15/2020
    Python Version: 3.7.3
    Purpose: Handles user CRUD operations on database 
"""


from datetime import datetime
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.core.config import settings
from src.core.utilities import fail_save, log_msg
from src.crud.base import CRUDBase
from src.crud.crud_stock import stock
from src.models.limit_order import LimitOrder
from src.models.long_position import LongPosition
from src.models.short_position import ShortPosition
from src.models.transaction import Transaction
from src.models.user import User
from src.models.watch_list import WatchList
from src.schemas.transaction import TradeType
from src.schemas.user import (LimitOrderCreate, TransactionCreate, UserCreate,
                              UserUpdate)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    Module for user/auth related CRUD operations
    """

    def get_all_users(self, db: Session) -> List[User]:
        return db.query(self.model.uid).distinct()

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

    def symbol_exist(self, db: Session, symbol_in: str):
        """
        Return True if the symbol exists
        """
        return  stock.get_stock_by_symbol(db=db, stock_symbol=symbol_in) != None

    @fail_save
    def add_to_watch_list(self, *, db: Session, user_in: User, symbol_in: str) -> User:
        """
        Add a watchlist to the user_in's watchlist.
        """
        # BUG: adding existing stocks breaks the code, handle it
        if self.symbol_exist(db=db, symbol_in=symbol_in):
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
        if self.symbol_exist(db=db, symbol_in=symbol_in):            
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
        if not self.symbol_in_exist(db=db, symbol_in=symbol_in):
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

        if not self.symbol_exist(db=db, symbol_in=symbol_in):
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

    @fail_save
    def create_order(
        self, *, db: Session, user_in: User, trade_type: TradeType, symbol: str, quantity: int, limit: float
    ) -> User:
        if self.symbol_exist(db=db, symbol_in=symbol):

            stc = LimitOrderCreate(
                user_id=user_in.uid,
                symbol=symbol,
                amount=quantity,
                t_type=trade_type.name,
                price=limit,
            )

            user_in.limit_orders.append(LimitOrder(**stc.__dict__))
        else:
            log_msg(
                f"Adding a non-existent symbol on limit order of User(uid = {user_in.uid}).",
                "WARNING",
            )
            return user_in

        db.commit()
        db.refresh(user_in)
        return user_in

    @fail_save
    def delete_order(self, *, db: Session, user_in: User, identity: int) -> User:
        std = None
        for order in user_in.limit_orders:
            if order.id == identity:
                std = order

        if std == None:
            log_msg(f"No limit order of id {identity} exists. ", "ERROR")
            return user_in
        else:
            user_in.limit_orders.remove(std)

        db.commit()
        db.refresh(user_in)

        return user_in

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

    def add_history(self, *, db: Session, user_in: User, price_in: float, trade_type_in: TradeType, amount_in: int, symbol_in: str) -> User:
        '''
        Add to the historical transaction.
        '''
        requested_record = TransactionCreate(
            user_id=user_in.uid, 
            price=price_in,
            action=trade_type_in.name, 
            symbol=symbol_in, 
            amount=amount_in
        )
        user_in.transaction_hist.append(Transaction(**requested_record.__dict__))
        db.commit()
        db.refresh(user_in)
        return user_in

        

user = CRUDUser(User)
