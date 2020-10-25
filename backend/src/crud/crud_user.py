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
# from src.core import trade
from src.core.config import settings
from src.core.utilities import fail_save, log_msg
from src.crud.base import CRUDBase
from src.crud.crud_stock import stock
from src.models.limit_order import LimitOrder
from src.models.long_position import LongPosition
from src.models.short_position import ShortPosition
from src.models.user import User
from src.models.watch_list import WatchList
from src.schemas.user import (LimitOrderCreate, TransactionCreate, UserCreate,
                              UserUpdate)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    Module for user/auth related CRUD operations
    """

    def get_all_users(self, db: Session) -> List[User]:
        return db.query(self.model.uid).distinct()

    def get_user_by_uid(self, db: Session, uid: str) -> Optional[User]:
        """
        Return the corresponding user by token.
        """
        return db.query(self.model).filter(self.model.uid == uid).first()  # Field is unique

    @fail_save
    def update_balance(self, db: Session, db_obj: User, u_balance: float) -> User:
        """
        Only update the balance of the user.
        """
        db_obj.balance = u_balance
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        pass

    def symbol_exist(self, db: Session, c_symbol: str):
        """
        Return True if the symbol exists
        """
        check = stock.get_stock_by_symbol(db=db, stock_symbol=c_symbol)

        return check != None

    @fail_save
    def add_to_watch_list(self, db: Session, user_in: User, w_symbol: str) -> User:
        """
        Add a watchlist to the user_in's watchlist.
        """
        # BUG: adding existing stocks breaks the code, handle it
        if self.symbol_exist(db=db, c_symbol=w_symbol):
            a_wl = WatchList(user_id=user_in.uid, symbol=w_symbol)

            user_in.watchlist.append(a_wl)
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
    def delete_from_watch_list(self, db: Session, user_in: User, w_symbol: str) -> User:
        """
        Delete a watchlist for user_in.
        """
        if self.symbol_exist(db=db, c_symbol=w_symbol):
            tbr = None
            for s in user_in.watchlist:
                if s.symbol == w_symbol:
                    tbr = s
                    break

            if tbr == None:
                log_msg(
                    f"Deleting a non-existent stock from watchlist of User(uid = {user_in.uid})",
                    "WARNING",
                )
            else:
                user_in.watchlist.remove(tbr)
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
        db: Session,
        user_in: User,
        t_type: str,
        p_symbol: str,
        p_amount: int,
        price: float,
    ) -> User:
        """
        Add amount and price to portfolio
        """
        if t_type != "long" and t_type != "short":
            log_msg(
                "No such type of transaction allowed, allowed are 'long' or'short'.",
                "ERROR",
            )
            return user_in

        if self.symbol_exist(db=db, c_symbol=p_symbol):

            ex = None
            ca = user_in.long_positions if t_type == "long" else user_in.short_positions

            # Compact portfolio
            for x in ca:
                if x.symbol == p_symbol:
                    ex = x
                    break

            if ex == None:
                a_wl = (
                    LongPosition(user_id=user_in.uid, symbol=p_symbol, amount=p_amount, avg=price)
                    if t_type == "long"
                    else ShortPosition(user_id=user_in.uid, symbol=p_symbol, amount=p_amount, avg=price)
                )
                user_in.long_positions.append(a_wl) if t_type == "long" else user_in.short_positions.append(a_wl)
            else:
                # running average used here
                new_avg = (ex.avg * ex.amount + p_amount * price) / (ex.amount + p_amount)
                new_amount = ex.amount + p_amount

                ex.avg, ex.amount = new_avg, new_amount

            db.commit()
            db.refresh(user_in)
            return user_in

        else:
            log_msg(
                f"Adding a non-existent symbol on portfolio of User(uid = {user_in.uid}).",
                "WARNING",
            )
            return user_in

    @fail_save
    def deduct_transaction(self, db: Session, user_in: User, t_type: str, p_symbol: str, p_amount: int) -> User:
        """
        Remove a stock from portfolio (selling). For type specify 'long' or 'short'
        """
        if t_type != "long" and t_type != "short":
            log_msg(
                "No such type of transaction allowed, allowed are 'long' or'short'.",
                "ERROR",
            )
            return user_in

        if self.symbol_exist(db=db, c_symbol=p_symbol):
            ex = None

            ca = user_in.long_positions if t_type == "long" else user_in.short_positions

            for x in ca:
                if x.symbol == p_symbol:
                    ex = x
                    break

            if ex == None:
                log_msg(
                    f"Deducting a non-existent stock of User(uid = {user_in.uid}).",
                    "WARNING",
                )
                return user_in
            else:

                new_amount = ex.amount - p_amount

                if new_amount < 0:
                    log_msg(
                        f"Deducting more than owned of User(uid = {user_in.uid}).",
                        "WARNING",
                    )
                elif new_amount == 0:
                    user_in.long_positions.remove(ex) if t_type == "long" else user_in.short_positions.remove(ex)
                else:
                    ex.amount = new_amount

                db.commit()
                db.refresh(user_in)
                return user_in

        else:
            log_msg(
                f"Adding a non-existent symbol on portfolio of User(uid = {user_in.uid}).",
                "WARNING",
            )
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
        self, *, db: Session, user_in: User, trade_type: str, symbol: str, quantity: int, limit: float
    ) -> User:

        allowed_types = ["buy", "sell", "short", "cover"]
        if self.symbol_exist(db=db, c_symbol=symbol):

            if trade_type not in allowed_types:
                log_msg(f"Trade type {trade_type} is not allowed", "ERROR")
                return user_in

            stc = LimitOrderCreate(
                user_id=user_in.uid,
                symbol=symbol,
                amount=quantity,
                t_type=trade_type,
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

    def reset_user_portfolio(self, user_in: User, db: Session) -> User:

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

    def add_transaction_history(self, db: Session, user_in: User, price_in: float ): 
        

user = CRUDUser(User)
