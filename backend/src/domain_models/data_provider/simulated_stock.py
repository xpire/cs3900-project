"""
Model for simulated stocks.
Formed by some predicatable and deterministic pattern for easier demonstrations
and testing.
All necessary information is mocked.
"""

import datetime as dt
from typing import List

from pydantic import BaseModel as BaseSchema
from src import crud
from src.core.utilities import as_delta
from src.schemas.exchange import Exchange


class Pattern(BaseSchema):
    datetime: dt.datetime
    open: float
    close: float
    exchange: Exchange

    def end_price(self, intraday=True):
        return self.intraday_price() if intraday else self.close

    def intraday_price(self):
        time = as_delta(self.datetime.time())
        open = self.exchange.open
        close = self.exchange.close

        if time < open:
            return None

        if time > close:
            return self.close

        progress = (time - open).seconds / (close - open).seconds
        return (self.close - self.open) * progress + self.open


# https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + dt.timedelta(n)


class StockSimulator:
    """
    Times treated by this class must be in the same timezone
    """

    def __init__(self, stock, day_patterns: List[float], pivot_date=None, volume=1000):
        self._symbol = stock.symbol

        self.exchange = crud.exchange.get_exchange_by_name(stock.exchange)

        # daily low, high, and volume
        self.patterns = day_patterns
        self.volume = volume

        # defines on which date day_patterns[0] occurs
        self.pivot_date = pivot_date or dt.date(2020, 1, 1)

    def make_request_by_days(self, end, days):
        intraday_data = self.intraday_data(end)

        if intraday_data is None:
            data = self.historical_data(end - dt.timedelta(days=days), end=end)
        else:
            data = self.historical_data(end - dt.timedelta(days=days - 1), end=end)
            data.append(intraday_data)

        data.reverse()
        return data

    def make_request(self, start, end):
        data = self.historical_data(start, end)
        intraday_data = self.intraday_data(end)

        if intraday_data is not None:
            data.append(intraday_data)

        data.reverse()
        return data

    def historical_data(self, start, end):
        return [self.day_data(d) for d in daterange(start, end)]

    def intraday_data(self, datetime):
        return self.day_data(datetime, intraday=True)

    def day_data(self, datetime, intraday=False):
        return self.generate_data(self.pattern_on_day(datetime), intraday)

    def generate_data(self, pattern: Pattern, intraday):
        end_price = pattern.end_price(intraday)

        if end_price is None:
            return None

        if pattern.open <= pattern.close:
            lo = pattern.open
            hi = end_price
        else:
            hi = pattern.open
            lo = end_price

        return dict(
            datetime=pattern.datetime,
            symbol=self.symbol,
            open=pattern.open,
            close=end_price,
            volume=self.volume,
            low=lo,
            high=hi,
        )

    def pattern_on_day(self, datetime):
        # works for negative numbers too
        open_idx = (datetime.date() - self.pivot_date).days % len(self.patterns)
        close_idx = (open_idx + 1) % len(self.patterns)

        return Pattern(
            datetime=datetime, open=self.patterns[open_idx], close=self.patterns[close_idx], exchange=self.exchange
        )

    @property
    def symbol(self):
        return self._symbol
