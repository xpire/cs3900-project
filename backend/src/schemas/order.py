from datetime import datetime
from typing import Any

from pydantic import BaseModel as BaseSchema
from src.schemas.transaction import TradeType
from src.util.auto_name_enum import AutoName
from src.util.extended_types import Const
from typing_extensions import Literal

# "id": order.id,
#             "name": order.stock_info.name,
#             "symbol": order.symbol,
#             "type": order.t_type,
#             "quantity": order.amount,
#             "price": order.price,
#             "exchange": order.stock_info.exchange,
#             "is_limit": True

# TODO check if this is even useful at all...
class Order(BaseSchema):
    # user: Any  # UserDM
    symbol: str
    name: str
    exchange: str
    trade_type: TradeType
    qty: int
    is_limit: bool
    # order_type: OrderType
