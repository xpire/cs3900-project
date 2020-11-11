"""
This file updates stock information every minute to allow live updates and day trading
"""

import time
from abc import abstractmethod
from datetime import datetime
from threading import Lock, Thread
from typing import List

from src import crud
from src.db.session import SessionThreadLocal
from src.schemas.time_series import TimeSeriesDBcreate

from .data_provider import DataProvider


class RepeatedUpdateProvider(DataProvider):
    """
    Update stock data repeatedly, where update time are determined
    by [repeat_in_x_seconds] (see RepeatScheduler)
    """

    def __init__(self, symbol_to_exchange, repeat_in_x_seconds, db, **kwargs):
        super().__init__(**kwargs)

        self._symbols = list(symbol_to_exchange.keys())
        self.symbol_to_exchange = symbol_to_exchange
        self.db = db

        self.repeat_in_x_seconds = repeat_in_x_seconds

        self._data = {}
        self.id = 0

        self.lock = Lock()

    def pre_start(self):
        crud.stock.remove_all_hist(db=self.db)

    def on_start(self):
        """
        Initialise db
        """
        data = self.get_init_data()
        print("===== INITIALISING MARKET DATA =====")
        for symbol, stock_data in data.items():
            print(f"Number of entries for {symbol}: {len(stock_data)}")
            time_series = stock_data_as_time_series(symbol, stock_data)
            crud.stock.update_time_series(db=self.db, symbol=symbol, time_series=time_series)
        print("===== FINISHED INITIALISATION =====")
        self.cache_latest_data(data)

        RepeatScheduler(self.update, self.repeat_in_x_seconds).start()

    @abstractmethod
    def get_init_data(self):
        """
        Returns data to initialise the db with
        """
        pass

    def update(self):
        """
        Retrieve data, update db and [self]'s cache
        """
        data = self.get_update_data()
        for symbol, stock_data in data.items():
            time_series = stock_data_as_time_series(symbol, stock_data)
            crud.stock.update_time_series(db=SessionThreadLocal(), symbol=symbol, time_series=time_series)
        self.cache_latest_data(data)
        self.notify()

    @abstractmethod
    def get_update_data(self):
        """
        Returns data to update the db with
        """
        pass

    def cache_latest_data(self, msg):
        """
        Cache part of the data so that they can be directly accessed without db
        """
        with self.lock:
            temp = {**self._data}  # shallow copy

        for symbol, data in msg.items():
            temp[symbol] = dict(
                curr_day_open=float(data[0]["open"]),
                curr_day_close=float(data[0]["close"]),
                prev_day_close=float(data[1]["close"]),
            )

        # switch out references
        with self.lock:
            self._data = temp
            self.id += 1

    @property
    def data_with_id(self):
        with self.lock:
            return (self._data, self.id)

    def get_stock(self, symbol):
        """
        Get stock given [symbol]
        """
        return crud.stock.get_by_symbol(db=self.db, symbol=symbol)

    @property
    def symbols(self):
        return self._symbols


def stock_data_as_time_series(symbol, stock_data) -> List[TimeSeriesDBcreate]:
    def to_timeseries_schema(day_data):
        return TimeSeriesDBcreate(
            date=day_data["datetime"],
            symbol=symbol,
            low=day_data["low"],
            high=day_data["high"],
            open=day_data["open"],
            close=day_data["close"],
            volume=day_data["volume"],
        )

    return [to_timeseries_schema(x) for x in stock_data]


def seconds_until_next_minute(at_second=15):
    """
    e.g. if at_second=15, return the number of seconds
    until the next minute, at the 15 seconds mark

    i.e.:
        - if now() is 10:05:10, then returns 10:06:15
        - if now() is 10:05:20, then returns 10:06:15
    """
    return 60 + at_second - datetime.now().second


class RepeatScheduler(Thread):
    """
    Repeatedly executes [callback] at times specified by [repeat_in_x_seconds],
    which could either be a function or a literal number
    """

    def __init__(self, callback, repeat_in_x_seconds):
        super().__init__()
        self.daemon = True
        self.callback = callback
        self.repeat_in_x_seconds = repeat_in_x_seconds

    def run(self):
        while True:
            if callable(self.repeat_in_x_seconds):
                x = self.repeat_in_x_seconds()
            else:
                x = self.repeat_in_x_seconds

            time.sleep(x)
            self.callback()
