"""
Statistic achievements
"""

from src.domain_models.account_stat_dm import AccountStat
from src.game.achievement.achievement import Achievement
from src.game.event.event import GameEventType
from src.game.event.sub_events import StatUpdateEvent

achievements = []

"""
BALANCE AND NET WORTH
"""


def ret_has_reached_balance(value):
    """Checks if the user has reached a certain balance

    Args:
        value (float): value to be reached
    """

    def has_reached_balance(e: StatUpdateEvent):
        return e.user.balance >= value

    return has_reached_balance


def ret_has_reached_net_worth(value):
    """Checks if the user has reached a certain net worth

    Args:
        value (float): value to be reached
    """

    def has_reached_net_worth(e: StatUpdateEvent):
        return AccountStat(e.user).net_worth() >= value

    return has_reached_net_worth


achievements.extend(
    [
        Achievement(
            id=2000,
            name="LOTS OF CA$H",
            description="Have balance over 150000",
            exp=20,
            event_type=GameEventType.STAT_UPDATE,
            can_unlock=ret_has_reached_balance(150000),
        ),
        Achievement(
            id=2010,
            name="Doubled up",
            description="Have net worth over 200000",
            exp=20,
            event_type=GameEventType.STAT_UPDATE,
            can_unlock=ret_has_reached_net_worth(200000),
        ),
        Achievement(
            id=2011,
            name="Millionaire",
            description="Have net worth over 10000000",
            exp=20,
            event_type=GameEventType.STAT_UPDATE,
            can_unlock=ret_has_reached_net_worth(10000000),
        ),
    ]
)

"""
POSITIONS
"""


def ret_has_n_positions(*, n, is_long):
    """Checks if the user has reached a certain number of positions

    Args:
        n (int): number of positions
        is_long (bool): True if checking for number of long positions, False for short
    """

    def has_n_positions(e: StatUpdateEvent):
        positions = e.user.model.long_positions if is_long else e.user.model.short_positions
        return len(positions) >= n

    return has_n_positions


achievements.extend(
    [
        Achievement(
            id=2100,
            name="This is so long",
            description="Have 3 or more long positions",
            exp=20,
            event_type=GameEventType.STAT_UPDATE,
            can_unlock=ret_has_n_positions(n=3, is_long=True),
        ),
        Achievement(
            id=2101,
            name="I got heaps of shorts",
            description="Have 3 or more short positions",
            exp=20,
            event_type=GameEventType.STAT_UPDATE,
            can_unlock=ret_has_n_positions(n=3, is_long=False),
        ),
    ]
)
