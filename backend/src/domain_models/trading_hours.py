from datetime import datetime, time

from pytz import timezone
from src.core.utilities import HTTP400


class TradingHoursManager:
    def __init__(self, trading_hours):
        self.trading_hours = trading_hours

    def get_trading_hours_info(self, stock):
        if stock.exchange not in self.trading_hours:
            raise HTTP400("Exchange for the given symbol not found.")

        curr_time = datetime.now().time()

        hours = self.trading_hours[stock.exchange]
        start, end = hours["start"], hours["end"]
        is_weekday = datetime.now(hours["timezone"]).weekday() <= 4
        is_trading = is_weekday and (start <= curr_time and curr_time <= end)
        return dict(is_trading=is_trading, start=start, end=end)


# Trading hours retrieved from
# https://www.thebalance.com/stock-market-hours-4773216#:~:text=Toronto%20Stock%20Exchange-,9%3A30%20a.m.%20to%204%20p.m.,30%20p.m.%20to%209%20p.m.&text=8%3A30%20a.m.%20to%203%20p.m.
trading_hours_manager = TradingHoursManager(
    dict(
        ASX=dict(start=time(23, 0), end=time(5, 0), timezone=timezone("Australia/Sydney")),
        NYSE=dict(start=time(13, 30), end=time(20, 0), timezone=timezone("America/New_York")),
        NASDAQ=dict(start=time(13, 30), end=time(20, 0), timezone=timezone("America/New_York")),
        LSE=dict(start=time(8, 0), end=time(16, 30), timezone=timezone("Europe/London")),
    )
)
