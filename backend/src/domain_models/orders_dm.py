import src.api.endpoints.stocks as stocks_api
from sqlalchemy.orm import Session
from src.core.utilities import log_msg
from src.crud.crud_user import user
from src.db.base_model import BaseModel
from src.game.achievement.achievement import UserAchievement
from src.game.setup.setup import achievements_list, level_manager
from src.models import UnlockedAchievement
from src.schemas import User, UserInDB

# class Name():

#     def update(self, data):
#         pass

# limit_trade_ex = Name()

# market_data_provider.subscribe(limit_trade_ex)


class pendingOrder:
    def update(self, data):
        pass
