from typing import List

from sqlalchemy.orm import Session
from src.crud.crud_user import user
from src.db.base_model import BaseModel
from src.game import level_manager
from src.schemas import User, UserInDB


# TODO move this and relevant imports somewhere
def update(model: BaseModel, db: Session):
    db.add(model)
    db.commit()
    db.refresh(model)


class UserDM:
    def __init__(self, user: User, db: Session):
        self.user = user
        self.db = db

    def add_exp(self, amount: float):
        level_manager.add_exp(self, amount)
        self.save_to_db()

    def unlock_achievement(self, achievement_id: int):
        print("unlock achievement:", achievement_id)

    def save_to_db(self):
        update(self.user, self.db)

    @property
    def exp(self):
        return self.user.exp

    @exp.setter
    def exp(self, exp: float):
        self.user.exp = exp

    @property
    def level(self):
        return self.user.level

    @level.setter
    def level(self, level: int):
        self.user.level = level

    @property
    def exp_until_next_level(self):
        return level_manager.exp_until_next_level(self)

    @property
    def is_max_level(self):
        return level_manager.is_max_level(self)

    @property
    def unlocked_achievement_ids(self):
        # return set(self.user.unlocked_achievements)
        return set([3])

    @property
    def schema(self):
        return User(
            **UserInDB.from_orm(self.user).__dict__,
            exp_until_next_level=self.exp_until_next_level,
            is_max_level=self.is_max_level
        )

    @property
    def model(self):
        return self.user

    def watchlist_create(self, wl_sys: str):
        self.user = user.add_to_watch_list(db=self.db, user_in=self.user, w_symbol=wl_sys)
        return self.user

    def watchlist_delete(self, wl_sys: str):
        self.user = user.delete_from_watch_list(db=self.db, user_in=self.user, w_symbol=wl_sys)
        return self.user
