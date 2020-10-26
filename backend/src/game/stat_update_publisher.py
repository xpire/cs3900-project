from src import crud
from src.domain_models.user_dm import UserDM
from src.game.event.sub_events import StatUpdateEvent
from src.game.setup.setup import event_hub


class StatUpdatePublisher:
    def __init__(self, db):
        self.db = db

    def update(self, data):
        user_models = crud.user.get_all_users(self.db)

        for user_m in user_models:
            event_hub.publish(StatUpdateEvent(user=UserDM(user_m, self.db)))
