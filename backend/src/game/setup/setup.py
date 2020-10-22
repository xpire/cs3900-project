from src.game.achievement.achievement_unlocker import AchievementUnlocker
from src.game.event.event_hub import EventHub
from src.game.level_manager import LevelManager
from src.game.setup.achievements_level_up import achievements as achievements_level_up
from src.game.setup.achievements_transaction import achievements as achievements_transaction
from src.game.setup.config import LEVEL_UP_EXPS
from src.notification import notif_hub

"""
ACHIEVEMENTS
"""

achievements_list = [*achievements_level_up, *achievements_transaction]
for x in achievements_list:
    print(x.name)

achievements = {x.id: x for x in achievements_list}

if len(achievements) != len(achievements_list):
    raise Exception("Duplicate achievements detected.")


"""
OBJECTS
"""
achievement_unlocker = AchievementUnlocker(achievements)

event_hub = EventHub()
event_hub.subscribe(achievement_unlocker)

level_manager = LevelManager(LEVEL_UP_EXPS, event_hub=event_hub, notif_hub=notif_hub)
