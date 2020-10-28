import datetime as dt
import itertools as it


# https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + dt.timedelta(n)


class SimulatedStock:
    """
    Times treated by this class must be in the same timezone
    """

    # TODO include dates in the output
    def __init__(
        self, symbol, exchange, trading_hours, day_lo, day_hi, pivot_date=None, rise_at_pivot=True, volume=1000
    ):
        self.symbol = symbol
        self.exchange = exchange
        self.trading_hours = trading_hours

        # daily low, high, and volume
        self.day_lo = day_lo
        self.day_hi = day_hi
        self.volume = volume

        # defines on which dates the stock rises/falls
        self.pivot_date = pivot_date or dt.datetime(2020, 1, 1)
        self.rise_at_pivot = rise_at_pivot

    def make_request_by_days(self, end, days):
        return self.make_request(self, start=end - dt.timedelta(days=days - 1), end=end)

    def make_request(self, start, end):
        # TODO if start, end same, what happens?
        response = self.historical_data(start, end)
        interday_data = self.interday_data(end)

        if interday_data is not None:
            response.append(interday_data)

        return response

    def historical_data(self, start, end):
        start = start.date()
        end = end.date()

        is_rising = self.is_rising_day(start)
        data = []
        for d in daterange(start, end):
            data.append(self.gen_data(d, is_rising))
            is_rising = not is_rising

        return data

    def interday_data(self, datetime):
        is_rising = self.is_rising_day(datetime)

        end_price = self.market_price_at(datetime.time(), is_rising)
        if end_price is None:
            return None

        return self.gen_data(datetime, is_rising, end_price)

    def market_price_at(self, time, is_rising):
        start, end = self.trading_hours

        if time < start:
            return None

        if time >= end:
            return self.day_hi if is_rising else self.day_lo

        progress = (time - start).minutes / (end - start).minutes

        if is_rising:
            day_start = self.day_lo
            day_change = self.day_hi - self.day_lo
        else:
            day_start = self.day_hi
            day_change = self.day_lo - self.day_hi

        return day_change * progress + day_start

    def gen_data(self, datetime, is_rising, end_price=None):
        end_price = self.day_hi if is_rising else self.day_lo
        if is_rising:
            return self.rising_data(self, datetime, end_price)
        else:
            return self.falling_data(self, datetime, end_price)

    def rising_data(self, datetime, end_price):
        return dict(
            datetime=datetime,
            symbol=self.symbol,
            open=self.day_lo,
            low=self.day_lo,
            high=end_price,
            close=end_price,
            volume=self.volume,
        )

    def falling_data(self, datetime, end_price):
        return dict(
            datetime=datetime,
            symbol=self.symbol,
            open=self.day_hi,
            low=end_price,
            high=self.day_hi,
            close=end_price,
            volume=self.volume,
        )

    def is_rising_day(self, date):
        # works for negative numbers too
        if (date - self.earliest_date).days % 2 == 0:
            return self.rise_at_start
        return not self.rise_at_start
