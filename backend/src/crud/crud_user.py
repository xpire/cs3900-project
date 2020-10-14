from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

# from backend.src.core.security import get_password_hash, verify_password
from backend.src.crud.base import CRUDBase
from backend.src.models.user import UserRet
from backend.src.schemas.user import UserCreate, UserUpdate

# a lot of things are kinda wrong here... need to rewrite kek
class CRUDUser(CRUDBase[UserRet, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[UserRet]:
        pass

    def create(self, db: Session, *, obj_in: UserCreate) -> UserRet:
        pass

    def update(
        self, db: Session, *, db_obj: UserRet, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> UserRet:
        pass

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[UserRet]:
        pass


user = CRUDUser(UserRet)
