"""
User Notification System
- Defines various notification events that carry info about notification to be sent
- Receives notifcation events and relays them to the client through a websocket
"""
from .notif_event import AchievementUnlockedEvent, FeatureUnlockedEvent, LevelUpEvent, UnlockableFeatureType
from .notifier import notif_hub
