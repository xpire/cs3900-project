import time
from abc import abstractmethod
from datetime import datetime
from threading import Lock, Thread
from typing import List

from src import crud
from src.schemas.time_series import TimeSeriesCreate

from .data_provider import DataProvider


class RepeatedUpdateProvider(DataProvider):
    """
    Update stock data repeatedly, where update time are determined
    by [repeat_in_x_seconds] (see RepeatScheduler)
    """

    def __init__(self, symbol_to_exchange, repeat_in_x_seconds, db, **kwargs):
        super().__init__(**kwargs)

        self.symbols = list(symbol_to_exchange.keys())
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
            # TODO test performance of this
            timeseries = stock_data_as_timeseries(symbol, stock_data)
            crud.stock.update_time_series(db=self.db, timeseries=timeseries)
            # crud.stock.batch_add_daily_time_series(db=self.db, stock=self.get_stock(symbol), time_series=stock_data)
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
            timeseries = stock_data_as_timeseries(symbol, stock_data)
            # TODO what is the difference between this one and the one above?
            crud.stock.update_time_series(db=self.db, timeseries=timeseries)
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
        return crud.stock.get_stock_by_symbol(db=self.db, symbol=symbol)


def stock_data_as_timeseries(symbol, stock_data) -> List[TimeSeriesCreate]:
    # try: TODO
    timeseries = []
    for day_data in stock_data:
        timeseries.append(
            TimeSeriesCreate(
                date=day_data["datetime"],
                symbol=symbol,
                low=day_data["low"],
                high=day_data["high"],
                open=day_data["open"],
                close=day_data["close"],
                volume=day_data["volume"],
            )
        )
    # except ValidationError as e:
    #     log_msg(f"Failed to update time series {e.__str__}.", "ERROR")
    #     return stock
    return timeseries


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
