"""
    File name: crud_user.py
    Author: Peiyu Tang
    Date created: 10/15/2020
    Python Version: 3.7.3
    Purpose: Handles user CRUD operations on database 
"""

from typing import Any, Dict, Optional, Union

# import src.models as md
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from src.core.config import settings

from src.crud.base import CRUDBase
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from src.models.watch_list import WatchList
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
        pass

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        pass

    def add_to_watch_list(self, db: Session, user_in: User, w_symbol: str) -> User:
        """
        Add a watchlist to the user's watchlist.
        """
        # BUG: doesnt handle case where w_symbol not a stock symbol, handle later maybe
        a_wl = WatchList(user_id=user_in.uid, symbol=w_symbol)

        user_in.watchlist.append(a_wl)
        db.commit()
        db.refresh(user_in)
        return user_in

    def delete_from_watch_list(
        self, db: Session, *, user_in: User, w_symbol: str
    ) -> User:
        """
        Delete a watchlist for this user.
        """
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


user = CRUDUser(User)
