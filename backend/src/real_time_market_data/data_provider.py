import time
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
from threading import Lock, Thread

from src import crud
from twelvedata import TDClient


class DataProvider(ABC):
    def __init__(self):
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.is_running = True
            self._start()

    @abstractmethod
    def _start(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractproperty
    def data(self):
        pass


class MarketDataProvider(DataProvider):
    def __init__(self, apikey, symbols, db, crud_obj):
        super().__init__()

        self.TD = TDClient(apikey=apikey)
        self.symbols = symbols
        self.db = db
        self.crud_obj = crud_obj

        self.request = self.create_request(days=2)

        self._data = {}
        self.lock = Lock()

        # send minutely updates
        self.observers = []

    def _start(self):
        self.batch_init()
        RepeatScheduler(self, seconds_until_next_minute).start()

    # Close sqlalchemy session
    def close(self):
        self.db.close()

    def batch_init(self):
        # Clear db first
        self.crud_obj.remove_all_hist(db=self.db)

        msg = self.make_request(self.create_request(days=365))

        for symbol, data in msg.items():
            stock = crud.stock.get_stock_by_symbol(db=self.db, stock_symbol=self.without_exchange(symbol))
            crud.stock.batch_add_daily_time_series(db=self.db, obj_in=stock, time_series_in=data)

        self.cache_latest_data(msg)

    def update(self):
        msg = self.make_request(self.request)

        # Insert into sqlite database
        for symbol, data in msg.items():
            stock = crud.stock.get_stock_by_symbol(self.db, self.without_exchange(symbol))
            crud.stock.update_time_series(db=self.db, obj_in=stock, u_time_series=data)

        self.cache_latest_data(msg)

        for observer in self.observers:
            observer.update(self.data)

    def subscribe(self, observer):
        self.observers.append(observer)

    def cache_latest_data(self, msg):
        with self.lock:
            for symbol, data in msg.items():
                symbol = self.without_exchange(symbol)
                self._data[symbol] = dict(
                    curr_day_open=data[0]["open"], curr_day_close=data[0]["close"], prev_day_close=data[1]["close"]
                )

    def create_request(self, days):
        return self.TD.time_series(
            symbol=self.symbols,
            interval="1day",
            outputsize=days,
            timezone="Australia/Sydney",  # output all timestamps in Sydney's timezone
        )

    def make_request(self, request):
        msg = request.as_json()
        if len(self.symbols) == 1:
            return {self.symbols[0]: msg}

        return msg

    def without_exchange(self, symbol):
        return symbol.split(":")[0]

    @property
    def data(self):
        with self.lock:
            return self._data


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
