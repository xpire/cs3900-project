from src.game import feature_unlocker
from src.game.event.event import GameEvent, GameEventType
from src.notification import FeatureUnlockedEvent, UnlockableFeatureType, notif_hub


class FeatureUnlocker:
    def update(self, event: GameEvent):
        if event.event_type is GameEventType.LEVEL_UP:
            event = self.unlock(event.user, event.new_level)

            if event is not None:
                notif_hub.publish(event)

    def unlock(self, user, level):
        if level == 3:
            return FeatureUnlockedEvent(
                user=user, feature_type=UnlockableFeatureType.LIMIT_ORDER, msg="You can now make limit orders!"
            )
        elif level == 5:
            return FeatureUnlockedEvent(
                user=user, feature_type=UnlockableFeatureType.SHORT_25, msg="You can now make short orders!"
            )
        elif level == 10:
            return FeatureUnlockedEvent(
                user=user,
                feature_type=UnlockableFeatureType.SHORT_50,
                msg="You can now short up to 50% of your net worth!",
            )
        return None


feature_unlocker = FeatureUnlocker()
