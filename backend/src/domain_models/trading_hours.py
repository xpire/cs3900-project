from datetime import datetime, timedelta

from pytz import timezone
from src import crud
from src.core.utilities import HTTP400


class TradingHoursManager:
    def get_trading_hours_info(self, stock):
        exchange = self.get_exchange(stock.exchange)
        curr_time = datetime.now(timezone(exchange.timezone))

        start = exchange.start
        end = exchange.end

        if start <= end:
            is_in_range = start <= curr_time and curr_time <= end
        else:
            is_in_range = start <= curr_time or curr_time <= end

        is_trading = is_in_range and self.is_trading_day(stock, curr_time.date())
        return dict(is_trading=is_trading, start=start, end=end)

    def is_trading_day(self, stock, date):
        exchange = self.get_exchange(stock.exchange)  # TODO this should later return a proper db object
        return exchange.simulated or date.weekday() <= 4

    def get_exchange(self, exchange):
        exchange = crud.exchange.get_exchange_by_name(exchange)
        if exchange is None:
            raise HTTP400("Exchange for the given symbol not found.")

        return exchange


def is_weekday(date):
    return date.weekday() <= 4


def next_weekday(date):
    days = 7 - date.weekday() if date.weekday() >= 4 else 1
    return date + timedelta(days=days)


def next_open(date_time, open_time):
    d = date_time.date()
    t = date_time.time()

    # if it is weekday and current time is before open, then next open is today at [open_time]
    # otherwise, next open is on next trading day at [open_time]
    if not (is_weekday(d) and t < open_time):
        d = next_weekday(d)

    return datetime.combine(d, open_time)


trading_hours_manager = TradingHoursManager()


# TEST CODE
# time1 = datetime.now() + timedelta(hours=9)
# open_time = time(10, 0)

# for i in range(10):
#     print("======")
#     print(time1, time1.weekday())
#     print(next_open(time1, open_time), next_open(time1, open_time).weekday())
#     time1 = time1 + timedelta(days=1)


"""
class TradingHoursManager:
    def __init__(self, trading_hours):
        self.trading_hours = trading_hours

    def get_trading_hours_info(self, stock):
        if stock.exchange not in self.trading_hours:
            raise HTTP400("Exchange for the given symbol not found.")

        curr_time = datetime.utcnow().time()

        hours = self.trading_hours[stock.exchange]
        start, end = hours["start"], hours["end"]
        is_weekday = datetime.now(hours["timezone"]).weekday() <= 4

        if start <= end:
            is_in_range = start <= curr_time and curr_time <= end
        else:
            is_in_range = start <= curr_time or curr_time <= end

        is_trading = is_weekday and is_in_range
        return dict(is_trading=is_trading, start=start, end=end)


# Trading hours retrieved from
# https://www.thebalance.com/stock-market-hours-4773216#:~:text=Toronto%20Stock%20Exchange-,9%3A30%20a.m.%20to%204%20p.m.,30%20p.m.%20to%209%20p.m.&text=8%3A30%20a.m.%20to%203%20p.m.
# TODO fix times, and make start and end times be according to their own timezones...?
trading_hours_manager = TradingHoursManager(
    dict(
        ASX=dict(start=time(23, 0), end=time(5, 0), timezone=timezone("Australia/Sydney")),
        NYSE=dict(start=time(13, 30), end=time(20, 0), timezone=timezone("America/New_York")),
        NASDAQ=dict(start=time(13, 30), end=time(20, 0), timezone=timezone("America/New_York")),
        LSE=dict(start=time(8, 0), end=time(16, 30), timezone=timezone("Europe/London")),
    )
)
"""
