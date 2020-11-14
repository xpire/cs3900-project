"""
Trading achievements
"""

from itertools import product

from src.game.achievement.achievement import Achievement
from src.game.event.event import GameEventType
from src.game.event.sub_events import TransactionEvent
from src.schemas.transaction import ClosingTransaction, OrderType, TradeType

achievements = []

"""
FIRST TRADES
"""


def ret_is_first_trade(*, trade_type, order_type):
    """Checks if it's the users first trade

    Args:
        trade_type (TradeType): type of trade
        order_type (OrderType): type of order
    """

    def is_first_trade(e: TransactionEvent):
        t = e.transaction
        return t.trade_type == trade_type and t.order_type == order_type

    return is_first_trade


def create_first_trade_achievements():
    """Achievements for performing certian trades for the first time

    Returns:
        List[Achievement]: list of achievements
    """
    START_ID = 3000

    data = {}
    data[(OrderType.MARKET, TradeType.BUY)] = dict(name="First market buy!", exp=10)
    data[(OrderType.MARKET, TradeType.SELL)] = dict(name="First market sell!", exp=10)
    data[(OrderType.MARKET, TradeType.SHORT)] = dict(name="First market short!", exp=10)
    data[(OrderType.MARKET, TradeType.COVER)] = dict(name="First market cover!", exp=10)
    data[(OrderType.LIMIT, TradeType.BUY)] = dict(name="First limit buy!", exp=10)
    data[(OrderType.LIMIT, TradeType.SELL)] = dict(name="First limit sell!", exp=10)
    data[(OrderType.LIMIT, TradeType.SHORT)] = dict(name="First limit short!", exp=10)
    data[(OrderType.LIMIT, TradeType.COVER)] = dict(name="First limit cover!", exp=10)

    xs = []
    for id, (order_type, trade_type) in enumerate(product(OrderType, TradeType), start=START_ID):
        xs.append(
            Achievement(
                id=id,
                **data[(order_type, trade_type)],
                description=f"Make your first {str(trade_type).lower()} {str(order_type).lower()} order",
                event_type=GameEventType.TRANSACTION,
                can_unlock=ret_is_first_trade(trade_type=trade_type, order_type=order_type),
            )
        )
    return xs


achievements.extend(create_first_trade_achievements())

"""
PROFITABLE TRADES
"""


def ret_is_profittable_trade(*, percentage):
    """Returns whether or not a trade was profitable

    Args:
        percentage (float): amount to be profitable by
    """

    def is_profittable_trade(e: TransactionEvent):
        if not isinstance(e.transaction, ClosingTransaction):
            return False
        return e.transaction.profit_percentage > percentage

    return is_profittable_trade


def ret_check_profit_percentage(*, check):
    """Checks how profitable a trade was

    Args:
        check (func): function to calculate whether or not a trade was profitable
    """

    def check_profit_percentage(e: TransactionEvent):
        if not isinstance(e.transaction, ClosingTransaction):
            return False
        return check(e.transaction.profit_percentage)

    return check_profit_percentage


achievements.extend(
    [
        Achievement(
            id=3100,
            name="First profit",
            description="Make a profit",
            exp=30,
            event_type=GameEventType.TRANSACTION,
            can_unlock=ret_check_profit_percentage(check=lambda p: p > 0),
        ),
        Achievement(
            id=3101,
            name="First loss",
            description="Make a loss",
            exp=5,
            event_type=GameEventType.TRANSACTION,
            can_unlock=ret_check_profit_percentage(check=lambda p: p < 0),
        ),
        Achievement(
            id=3110,
            name="Big profit maker",
            description="Make a profit of over 0.1%",
            exp=50,
            event_type=GameEventType.TRANSACTION,
            can_unlock=ret_check_profit_percentage(check=lambda p: p > 0.1),
        ),
        Achievement(
            id=3111,
            name="Be my fund manager",
            description="Make a profit of over 1%",
            exp=50,
            event_type=GameEventType.TRANSACTION,
            can_unlock=ret_check_profit_percentage(check=lambda p: p > 1),
        ),
        Achievement(
            id=3120,
            name="Ouch",
            description="Make a loss of over 0.1%",
            exp=5,
            event_type=GameEventType.TRANSACTION,
            can_unlock=ret_check_profit_percentage(check=lambda p: p < -0.1),
        ),
    ]
)
