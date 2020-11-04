from src.game.event.event import GameEvent, GameEventType
from src.notification import FeatureUnlockedEvent, UnlockableFeatureType, notif_hub


class FeatureUnlocker:
    def __init__(self, features):
        self.features = features

    def update(self, event: GameEvent):
        if event.event_type is GameEventType.LEVEL_UP:
            event = self.unlock(event.user, event.new_level)

            if event is not None:
                notif_hub.publish(event)

    def unlock(self, user, level):
        for feature_type, info in self.features.items():
            if info["level"] == level:
                return FeatureUnlockedEvent(user=user, feature_type=feature_type, msg=info["level"])
        return None

    def level_required(self, feature_type):
        info = self.features.get(feature_type, None)
        if info is None:
            return None
        return info["level"]


features = {
    UnlockableFeatureType.LIMIT_ORDER: dict(level=3, msg="You can now make limit orders!"),
    UnlockableFeatureType.SHORT_25: dict(level=5, msg="You can now make short orders!"),
    UnlockableFeatureType.SHORT_50: dict(level=10, msg="You can now short up to 50% of your net worth!"),
}

feature_unlocker = FeatureUnlocker(features)
