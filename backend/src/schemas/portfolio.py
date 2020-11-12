"""
Schema for the users portfolio
"""

from typing import List

from pydantic import BaseModel as BaseSchema


class PositionAPIout(BaseSchema):
    symbol: str
    name: str
    price: float
    previous_price: float
    owned: int
    average_paid: float
    total_paid: float
    value: float
    profit: float
    day_profit: float
    day_return: float
    total_return: float


class PortfolioAPIout(BaseSchema):
    long: List[PositionAPIout]
    short: List[PositionAPIout]


class PortfolioStatAPIout(BaseSchema):
    # closing values
    total_long_value: float
    total_short_value: float
    total_portfolio_value: float

    # profit
    total_long_profit: float
    total_short_profit: float
    total_portfolio_profit: float

    # return
    total_long_return: float
    total_short_return: float
    total_portfolio_return: float

    # daily profit
    daily_long_profit: float
    daily_short_profit: float
    daily_portfolio_profit: float

    # daily return
    daily_long_return: float
    daily_short_return: float
    daily_portfolio_return: float

    # other
    balance: float
    short_balance: float
    total_value: float
