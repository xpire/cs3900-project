from src.game.achievement.achievement import Achievement
from src.game.event.event import GameEventType
from src.game.event.sub_events import StatUpdateEvent

achievements = []
"""
PROFITABLE TRADE
"""


def ret_has_reached_balance(value):
    def has_reached_balance(e: StatUpdateEvent):
        return e.user.balance >= value

    return has_reached_balance


def ret_has_reached_net_worth(value):
    def has_reached_net_worth(e: StatUpdateEvent):
        return e.user.get_net_value() >= value

    return has_reached_net_worth


"""
others:
- number of long positions, short positions
- value of long positions / short positions
"""

achievements.extend(
    [
        Achievement(
            id=400,
            name="Test",
            description="Have balance less than 10000",
            exp=20,
            event_type=GameEventType.TRANSACTION,
            can_unlock=lambda e: e.user.balance < 10000,
        ),
        Achievement(
            id=300,
            name="Sugar daddy",
            description="Have balance over 10001",
            exp=20,
            event_type=GameEventType.TRANSACTION,
            can_unlock=ret_has_reached_balance(10001),
        ),
        Achievement(
            id=301,
            name="$$$",
            description="Have balance over 50000",
            exp=20,
            event_type=GameEventType.TRANSACTION,
            can_unlock=ret_has_reached_balance(50000),
        ),
        Achievement(
            id=310,
            name="Double up",
            description="Have net worth over 20000",
            exp=20,
            event_type=GameEventType.TRANSACTION,
            can_unlock=ret_has_reached_net_worth(20000),
        ),
        Achievement(
            id=311,
            name="Millionaire",
            description="Have net worth over 10000000",
            exp=20,
            event_type=GameEventType.TRANSACTION,
            can_unlock=ret_has_reached_net_worth(10000000),
        ),
    ]
)
