"""
    File name: crud_user.py
    Author: Peiyu Tang
    Date created: 10/15/2020
    Python Version: 3.7.3
    Purpose: Handles user CRUD operations on database 
"""

from typing import Optional

# import src.models as md
from sqlalchemy.orm import Session
from src.core.config import settings

from src.crud.base import CRUDBase
from src.crud.crud_stock import stock
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from src.models.watch_list import WatchList
from src.models.portfolio import Portfolio
from src.core.utilities import log_msg


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    Module for user/auth related CRUD operations
    """

    def get_user_by_uid(self, db: Session, *, uid: str) -> Optional[User]:
        """
        Return the corresponding user by token.
        """
        return (
            db.query(self.model).filter(self.model.uid == uid).first()
        )  # Field is unique

    def update_balance(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        """
        Only update the balance of the user.
        """
        db_obj.balance = obj_in.balance
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        pass

    def symbol_exist(self, db: Session, c_symbol: str):
        """
        Return True if the symbol exists
        """
        check = stock.get_stock_by_symbol(db=db, stock_symbol=c_symbol)

        return True if (check != None) else False

    def add_to_watch_list(self, db: Session, user_in: User, w_symbol: str) -> User:
        """
        Add a watchlist to the user_in's watchlist.
        """
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

    def delete_from_watch_list(
        self, db: Session, *, user_in: User, w_symbol: str
    ) -> User:
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

    def add_to_portfolio(
        self, db: Session, *, user_in: User, p_symbol: str, p_amount: int, price: float
    ) -> User:
        """
        Add to portfolio
        """
        if self.symbol_exist(db=db, c_symbol=p_symbol):

            ex = None
            # Compact portfolio
            for x in user_in.portfolios:
                if x.symbol == p_symbol:
                    ex = x
                    break

            if ex == None:
                a_wl = Portfolio(
                    user_id=user_in.uid, symbol=p_symbol, amount=p_amount, avg=price
                )
                user_in.portfolios.append(a_wl)
                db.commit()
                db.refresh(user_in)
                return user_in
            else:
                # running average used here
                new_avg = (ex.avg * ex.amount + p_amount * price) / (
                    ex.amount + p_amount
                )
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

    def deduct_from_portfolio(
        self, db: Session, *, user_in: User, p_symbol: str, p_amount: int
    ) -> User:
        """
        Remove a stock from portfolio (selling).
        """
        if self.symbol_exist(db=db, c_symbol=p_symbol):
            ex = None
            for x in user_in.portfolios:
                if x.symbol == p_symbol:
                    ex = x
                    break

            if ex == None:
                log_msg(
                    f"Deducting a non-existent stock on portfolio of User(uid = {user_in.uid}).",
                    "WARNING",
                )
                return user_in
            else:

                new_amount = ex.amount - p_amount

                if new_amount < 0:
                    log_msg(
                        f"Deducting more than owned on porfolio of User(uid = {user_in.uid}).",
                        "WARNING",
                    )
                elif new_amount == 0:
                    user_in.portfolios.remove(ex)
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


user = CRUDUser(User)
