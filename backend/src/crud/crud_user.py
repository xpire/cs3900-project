'''
    File name: crud_user.py
    Author: Peiyu Tang
    Date created: 10/15/2020
    Python Version: 3.7.3
    Purpose: Handles user CRUD operations on database 
'''

from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from backend.src.db.session import SessionLocal
from backend.src.core.config import settings
import backend.src.models as md  

from backend.src.crud.base import CRUDBase
from backend.src.models.user import User
from backend.src.schemas.user import UserCreate, UserUpdate, 

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    '''
    Module for user/auth related CRUD operations 
    '''
    'something'
    def get_user_by_token(self, db: Session, *, token: str) -> Optional[User]:
        '''
        Return the corresponding user by token.
        '''
        return db.query(self.model).filter(self.model.token == str).first() # Field is unique 

    def create_and_give_balance(self, db: Session, *, obj_in: UserCreate) -> str:
        pass

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> UserRet:
        pass

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        pass


user = CRUDUser(User)
