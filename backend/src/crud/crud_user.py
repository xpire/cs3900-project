"""
    File name: crud_user.py
    Author: Peiyu Tang
    Date created: 10/15/2020
    Python Version: 3.7.3
    Purpose: Handles user CRUD operations on database 
"""

from typing import Any, Dict, Optional, Union

# import src.models as md
from sqlalchemy.orm import Session
from src.core.config import settings
from src.crud.base import CRUDBase
from src.db.session import SessionLocal
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    Module for user/auth related CRUD operations
    """

    "something"

    def get_user_by_token(self, db: Session, *, uid: str) -> Optional[User]:
        """
        Return the corresponding user by token.
        """
        return db.query(self.model).filter(self.model.uid == uid).first()  # Field is unique

    def update_balance(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        """
        Only update the balance of the user.
        """
        pass

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        pass

    def delete_user_by_email(self, db: Session, *, email: str) -> bool:
        obj = db.query(self.model).filter(self.model.email == email).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False


user = CRUDUser(User)
