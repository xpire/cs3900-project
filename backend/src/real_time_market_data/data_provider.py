import time
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
from threading import Thread

from src import crud

"""
TODO
- helper functions (crud?/not) to separate between simulated and non-simulated
- focus on refactoring in the next sprint
- how to test limit order execution etc.
- limit order test: don't use latest data, but use lo and high since we get data
in blocks of 5
- need to return open, high. low, close, volume, etc. - define schema
    - constant volume
    - high and low update accordingly
    - make high and low more predictable
- server needs to tick at much higher speed, e.g. every 15 seconds
- confirmation message: Executed at ... / positions on the stock?
- after you trade, we want to see changes to the balance, networth, short/long networths,
and portfolio
- portfolio - inventory system: hover to see more details, click for even more
- floaty + button?

- change days=365 -> time-start, time-end for yearly data, keep it at days=2 for other
"""


class DataProvider(ABC):
    def __init__(self, db, symbol_to_exchange):
        self.is_running = False
        self.callbacks = []

        self.symbols = list(symbol_to_exchange.keys())
        self.symbol_to_exchange = symbol_to_exchange
        self.db = db

    def pre_start(self):
        pass

    def start(self):
        """
        Start retrieving data
        """
        if not self.is_running:
            self.is_running = True
            self.on_start()

    @abstractmethod
    def on_start(self):
        """
        Executes upon start()
        """
        pass

    def get_stock(self, symbol):
        return crud.stock.get_stock_by_symbol(db=self.db, stock_symbol=symbol)

    def subscribe(self, callback):
        """
        Subscribe [observer] to regular updates
        """
        callback(self.data)  # remove the argument passed in (?)
        self.callbacks.append(callback)

    def notify(self):
        for callback in self.callbacks:
            callback(self.data)

    @property
    def data(self):
        return self.data_with_id[0]

    @abstractproperty
    def data_with_id(self):
        """
        Return new id for every new data, for caching purposes
        """
        pass

    def get_curr_day_close(self, symbol):
        return self.data[symbol]["curr_day_close"]

    def get_curr_day_open(self, symbol):
        return self.data[symbol]["curr_day_open"]

    def get_prev_day_close(self, symbol):
        return self.data[symbol]["prev_day_close"]


class MarketDataProvider(DataProvider):
    def __init__(self, provider, **kwargs):
        super().__init__(**kwargs)
        self.provider = provider
        provider.subscribe(self.notify)
        self.is_running = False

    def start(self):
        # TODO erase db

        if not self.is_running:
            self.is_running = True
            self.provider.pre_start()
            self.provider.start()

    @property
    def data_with_id(self):
        return self.provider.data_with_id


class RepeatedPollingProvider(DataProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._data = {}
        self.id = 0

    def pre_start(self):
        # remove history
        pass

    def on_start(self):
        self.init_data()

    def init_data(self):
        data = self.get_init_data()
        print("===== INITIALISING MARKET DATA =====")
        for symbol, stock_data in data.items():
            print(f"Number of entries for {symbol}: {len(stock_data)}")
            crud.stock.batch_add_daily_time_series(
                db=self.db, stock_in=self.get_stock(symbol), time_series_in=stock_data
            )
        print("===== FINISHED INITIALISATION =====")
        self.cache_latest_data(data)

    @abstractmethod
    def get_init_data(self):
        """
        Returns data to initalise db with upon start
        """
        pass

    def update(self):
        data = self.get_update_data()
        for symbol, stock_data in data.items():
            crud.stock.update_time_series(db=self.db, stock_in=self.get_stock(symbol), u_time_series=stock_data)
        self.cache_latest_data(data)

        for observer in self.observers:
            observer.update(self.data)  # remove this parameter

    @abstractmethod
    def get_update_data(self):
        pass

    def cache_latest_data(self, msg):
        temp = {**self._data}
        for symbol, data in msg.items():
            # symbol = self.without_exchange(symbol)
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


def seconds_until_next_minute(poll_at_second=15):
    return 60 + poll_at_second - datetime.now().second


class RepeatScheduler(Thread):
    def __init__(self, provider, wait_for_x_seconds):
        super().__init__()
        self.daemon = True
        self.provider = provider
        self.wait_for_x_seconds = wait_for_x_seconds

    def run(self):
        while True:
            if callable(self.wait_for_x_seconds):
                x = self.wait_for_x_seconds()
            else:
                x = self.wait_for_x_seconds

            time.sleep(x)
            self.provider.update()
