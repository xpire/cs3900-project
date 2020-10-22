from itertools import product

from src.game.achievement.achievement import Achievement
from src.game.event.event import GameEventType
from src.game.event.sub_events import TransactionEvent
from src.schemas.transaction import ClosingTransaction, OrderType, TradeType

achievements = []

"""
FIRST TRADE
"""


def ret_is_first_trade(*, trade_type, order_type):
    def is_first_trade(e: TransactionEvent):
        t = e.transaction
        return t.trade_type == trade_type and t.order_type == order_type

    return is_first_trade


def create_first_trade_achievements():
    START_ID = 10

    data = {}
    data[(OrderType.MARKET, TradeType.BUY)] = dict(name="First market buy!", exp=10)
    data[(OrderType.MARKET, TradeType.SELL)] = dict(name="First market sell!", exp=10)
    data[(OrderType.MARKET, TradeType.SHORT)] = dict(name="First market short!", exp=20)
    data[(OrderType.MARKET, TradeType.COVER)] = dict(name="First market cover!", exp=20)
    data[(OrderType.LIMIT, TradeType.BUY)] = dict(name="First limit buy!", exp=20)
    data[(OrderType.LIMIT, TradeType.SELL)] = dict(name="First limit sell!", exp=20)
    data[(OrderType.LIMIT, TradeType.SHORT)] = dict(name="First limit short!", exp=30)
    data[(OrderType.LIMIT, TradeType.COVER)] = dict(name="First limit cover!", exp=30)

    xs = []
    for id, (order_type, trade_type) in enumerate(product(OrderType, TradeType), start=START_ID):
        xs.append(
            Achievement(
                id=id,
                **data[(order_type, trade_type)],
                description=f"Make your first {trade_type} {order_type} order",  # TODO make another function to prettify
                event_type=GameEventType.TRANSACTION,
                can_unlock=ret_is_first_trade(trade_type=trade_type, order_type=order_type),
            )
        )
    return xs


achievements.extend(create_first_trade_achievements())

"""
PROFITABLE TRADE
"""


def ret_is_profittable_trade(*, percentage):
    def is_profittable_trade(e: TransactionEvent):
        if not isinstance(e.transaction, ClosingTransaction):
            return False
        return e.transaction.profit_percentage >= percentage

    return is_profittable_trade


achievements.extend(
    [
        Achievement(
            id=20,
            name="Profit maker",
            description="Make profit of over 5%",
            exp=20,
            event_type=GameEventType.TRANSACTION,
            can_unlock=ret_is_profittable_trade(percentage=5),
        ),
    ]
)
