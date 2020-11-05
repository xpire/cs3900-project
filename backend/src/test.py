from enum import Enum


class TradeType(str, Enum):
    BUY = (True, True, True)
    SELL = (False, True, False)
    SHORT = (False, True, False)
    COVER = (False, True, False)

    def __new__(cls, is_buying, is_long, is_opening):
        obj = str.__new__(cls)
        obj._value_ = None
        obj.is_buying = is_buying
        obj.is_long = is_long
        obj.is_opening = is_opening
        return obj

    def __init__(self, *args):
        self._value_ = self._name_


# from fastapi.encoders import jsonable_encoder
# from pydantic import BaseModel as BaseSchema


# class Base(BaseSchema):
#     symbol: str
#     trade_type: TradeType


print(TradeType.BUY.value)
print(TradeType.BUY.name)
print(TradeType.SELL.is_buying)
print(TradeType.SELL.is_long)
print(TradeType.SELL.is_opening)
