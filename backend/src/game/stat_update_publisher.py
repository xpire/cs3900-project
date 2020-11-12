"""
Helper to notify the event hub of any updates to the statistics page
"""

from src import crud
from src.db.session import SessionThreadLocal
from src.domain_models.user_dm import UserDM
from src.game.event.sub_events import StatUpdateEvent
from src.game.setup.setup import event_hub


class StatUpdatePublisher:
    def update(self):
        db = SessionThreadLocal()
        user_models = crud.user.get_all_users(db=db)

        for user_m in user_models:
            event_hub.publish(StatUpdateEvent(user=UserDM(user_m, db)))
