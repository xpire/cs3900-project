from datetime import datetime, time, timedelta

from pytz import timezone
from src import crud, schemas
from src.core.utilities import as_delta
from src.schemas.response import Fail


class TradingHoursManager:
    def is_trading(self, stock) -> bool:
        """Checks if a stock is currently in its trading hours

        Args:
            stock (Stock): stock object

        Returns:
            bool: True if in trading hours
        """
        exchange = self.get_exchange(stock.exchange)
        curr_datetime = datetime.now(timezone(exchange.timezone))
        date, time = curr_datetime.date(), as_delta(curr_datetime.time())

        open = exchange.open
        close = exchange.close

        is_in_range = open <= time and time <= close
        return is_in_range and self.is_trading_day(stock, date)

    def get_trading_hours_info(self, stock) -> schemas.TradingHoursInfo:
        """Gets the trading hour information for a stock

        Args:
            stock (Stock): stock object

        Returns:
            schemas.TradingHoursInfo: information about the stocks trading hours
        """
        exchange = self.get_exchange(stock.exchange)
        is_trading = self.is_trading(stock)
        return schemas.TradingHoursInfo(is_trading=is_trading, open=exchange.open, close=exchange.close)

    def is_trading_day(self, stock, date):
        """Checks if provided date is a trading day

        Args:
            stock (Stock): a stock object
            date (datetime.date): date to check

        Returns:
            [type]: [description]
        """
        exchange = self.get_exchange(stock.exchange)
        return exchange.simulated or date.weekday() <= 4

    def get_exchange(self, exchange):
        """returns the exchange object from exchange name

        Args:
            exchange (str): exchange name

        Returns:
            Result: Success/Fail
        """
        exchange = crud.exchange.get_exchange_by_name(exchange)
        if exchange is None:
            return Fail("Exchange for the given symbol not found.").ok()
        return exchange


def is_weekday(date):
    """Checks if given date is a weekday

    Args:
        date (datetime.date): date to check

    Returns:
        bool: True if weekday
    """
    return date.weekday() <= 4


def next_weekday(date):
    """Finds the next weekday from provided date

    Args:
        date (datetime.date): date to check from

    Returns:
        datetime.date: date of next weekday
    """
    days = 7 - date.weekday() if date.weekday() >= 4 else 1
    return date + timedelta(days=days)


def next_open(datetime, exchange):
    """Finds the next opening date and time of an exchange

    Args:
        datetime (datetime.datetime): datetime to check from
        exchange (Exchange): exchange object

    Returns:
        datetime.datetime: datetime of next opening
    """
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
