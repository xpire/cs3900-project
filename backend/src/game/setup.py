# from __future__ import annotations
from itertools import product

from pydantic import Field
from src.game.achievement import Achievement, AchievementData
from src.game.achievement_unlocker import AchievementUnlocker
from src.game.event import GameEvent, GameEventType
from src.game.event_hub import EventHub
from src.schemas.transaction import ClosingTransaction, OrderType, TradeType, Transaction
from src.util.extended_types import Const

"""
EVENTS
"""


class TransactionEvent(GameEvent):
    event_type: GameEventType = Const(GameEventType.TRANSACTION)
    transaction: Transaction


class LevelUpEvent(GameEvent):
    event_type: GameEventType = Const(GameEventType.LEVEL_UP)
    new_level: int


class AchievementUnlockedEvent(GameEvent):
    event_type: GameEventType = Const(GameEventType.ACHIEVEMENT_UNLOCKED)
    achievement: Achievement


"""
ACHIEVEMENTS
"""


def ret_has_reached_level(level):
    def has_reached_level(e: LevelUpEvent):
        return e.new_level == level

    return has_reached_level


def ret_is_first_trade(*, trade_type, order_type):
    def is_first_trade(e: TransactionEvent):
        t = e.transaction
        return t.trade_type == trade_type and t.order_type == order_type

    return is_first_trade


def ret_is_profittable_trade(*, percentage):
    def is_profittable_trade(e: TransactionEvent):
        if not isinstance(e.transaction, ClosingTransaction):
            return False
        return e.transaction.profit_percentage >= percentage

    return is_profittable_trade


achievements_list = [
    Achievement(
        id=1,
        name="Good start",
        description="Reach level 3",
        exp=10,
        event_type=GameEventType.LEVEL_UP,
        can_unlock=ret_has_reached_level(3),
    ),
    Achievement(
        id=2,
        name="Halfway there!",
        description="Reach level 5",
        exp=60,
        event_type=GameEventType.LEVEL_UP,
        can_unlock=ret_has_reached_level(5),
    ),
    Achievement(
        id=20,
        name="Profit maker",
        description="Make profit of over 5%",
        exp=20,
        event_type=GameEventType.TRANSACTION,
        can_unlock=ret_is_profittable_trade(percentage=5),
    ),
]

data = {}
data[(OrderType.MARKET, TradeType.BUY)] = dict(name="First market buy!", exp=10)
data[(OrderType.MARKET, TradeType.SELL)] = dict(name="First market sell!", exp=10)
data[(OrderType.MARKET, TradeType.SHORT)] = dict(name="First market short!", exp=20)
data[(OrderType.MARKET, TradeType.COVER)] = dict(name="First market cover!", exp=20)
data[(OrderType.LIMIT, TradeType.BUY)] = dict(name="First limit buy!", exp=20)
data[(OrderType.LIMIT, TradeType.SELL)] = dict(name="First limit sell!", exp=20)
data[(OrderType.LIMIT, TradeType.SHORT)] = dict(name="First limit short!", exp=30)
data[(OrderType.LIMIT, TradeType.COVER)] = dict(name="First limit cover!", exp=30)

first_trade_achievements = []
for id, (order_type, trade_type) in enumerate(product(OrderType, TradeType), start=10):
    first_trade_achievements.append(
        Achievement(
            id=id,
            **data[(order_type, trade_type)],
            description=f"Make your first {trade_type} {order_type} order",  # TODO make another function to prettify
            event_type=GameEventType.TRANSACTION,
            can_unlock=ret_is_first_trade(trade_type=trade_type, order_type=order_type),
        )
    )

achievements_list.extend(first_trade_achievements)
achievements = {x.id: x for x in achievements_list}

if len(achievements) != len(achievements_list):
    raise Exception("Duplicate achievements detected.")

"""
OBJECTS
"""
achievement_unlocker = AchievementUnlocker(achievements)

event_hub = EventHub()
event_hub.subscribe(achievement_unlocker)
