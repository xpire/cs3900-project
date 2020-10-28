import datetime as dt
import itertools as it


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

        # template, TODO may not be needed...
        self.rise_day = self.rising_data(end_price=day_hi)
        self.fall_day = self.falling_data(end_price=day_lo)

    def make_request_by_days(self, end, days):
        return self.make_request(self, start=end - dt.timedelta(days=days - 1), end=end)

    def make_request(self, start, end):
        # TODO if start, end same, what happens?
        response = self.historical_data(start, end - dt.timedelta(days=1))
        interday_data = self.interday_data(end)

        if interday_data is not None:
            response.append(interday_data)

        return response

    def historical_data(self, start, end):
        days = (end.date() - start.date()).days
        order = (self.rise_day, self.fall_day) if self.is_rising_day(start) else (self.fall_day, self.rise_day)
        return it.islice(it.cycle(order), stop=days)

    def interday_data(self, date_time):
        is_rising = self.is_rising_day(date_time)

        price = self.market_price_at(date_time.time(), is_rising)
        if price is None:
            return None

        if is_rising:
            return self.rising_data(end_price=price)
        else:
            return self.falling_data(end_price=price)

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

    def rising_data(self, end_price):
        return dict(
            symbol=self.symbol, open=self.day_lo, low=self.day_lo, high=end_price, close=end_price, volume=self.volume
        )

    def falling_data(self, end_price):
        return dict(
            symbol=self.symbol, open=self.day_hi, low=end_price, high=self.day_hi, close=end_price, volume=self.volume
        )

    def is_rising_day(self, date):
        # works for negative numbers too
        if (date - self.earliest_date).days % 2 == 0:
            return self.rise_at_start
        return not self.rise_at_start
