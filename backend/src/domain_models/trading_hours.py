from datetime import datetime, time, timedelta

from pytz import timezone
from src import crud, schemas
from src.core.utilities import as_delta
from src.schemas.response import Fail


class TradingHoursManager:
    def is_trading(self, stock) -> bool:
        exchange = self.get_exchange(stock.exchange)
        curr_datetime = datetime.now(timezone(exchange.timezone))
        date, time = curr_datetime.date(), as_delta(curr_datetime.time())

        open = exchange.open
        close = exchange.close

        is_in_range = open <= time and time <= close
        return is_in_range and self.is_trading_day(stock, date)

    def get_trading_hours_info(self, stock) -> schemas.TradingHoursInfo:
        exchange = self.get_exchange(stock.exchange)
        is_trading = self.is_trading(stock)
        return schemas.TradingHoursInfo(is_trading=is_trading, open=exchange.open, close=exchange.close)

    def is_trading_day(self, stock, date):
        exchange = self.get_exchange(stock.exchange)
        return exchange.simulated or date.weekday() <= 4

    def get_exchange(self, exchange):
        exchange = crud.exchange.get_exchange_by_name(exchange)
        if exchange is None:
            return Fail("Exchange for the given symbol not found.").ok()
        return exchange


def is_weekday(date):
    return date.weekday() <= 4


def next_weekday(date):
    days = 7 - date.weekday() if date.weekday() >= 4 else 1
    return date + timedelta(days=days)


def next_open(datetime, exchange):
    d = datetime.date()
    t = as_delta(datetime.time())

    # if it is weekday and current time is before open, then next open is today at [open_time]
    # otherwise, next open is on next trading day at [open_time]
    if exchange.simulated:
        if t >= exchange.open:
            d += timedelta(days=1)
    else:
        if not is_weekday(d) or t >= exchange.open:
            d = next_weekday(d)

    return datetime.combine(d, time(0)) + exchange.open


trading_hours_manager = TradingHoursManager()
