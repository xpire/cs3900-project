import json
import time
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime, timedelta
from threading import Timer, Lock, Thread
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


class CompositeDataProvider(DataProvider):
    def __init__(self, providers):
        super().__init__()
        self.providers = providers

    def _start(self):
        for p in self.providers:
            p.start()

    def update(self):
        pass

    @property
    def data(self):
        data = {}
        for p in self.providers:
            data = {**data, **p.data}
        return data


class RealTimeDataProvider(DataProvider):
    def __init__(self, apikey, symbols):
        super().__init__()

        self.TD = TDClient(apikey="a603f4e94a3f4ebc8116636cd8e6aaba")
        self.symbols = symbols

        self.request = self.TD.time_series(
            symbol=symbols,
            interval="1min",
            outputsize=1,
            timezone="Australia/Sydney",  # output all timestamps in Sydney's timezone
        )
        self._data = {}
        self.lock = Lock()

    def _start(self):
        RepeatScheduler(self, seconds_until_next_minute).start()

    def update(self):
        message = self.request.as_json()
        if len(self.symbols) == 1:
            message = {self.symbols[0]: message}

        with self.lock:
            for symbol, data in message.items():
                self._data[symbol] = dict(
                    close=data[0]["close"], datetime=data[0]["datetime"]
                )

    @property
    def data(self):
        with self.lock:
            return self._data


class SimulatedDataProvider(DataProvider):
    def __init__(self, stocks, interval=5):
        super().__init__()

        self.stocks = stocks
        self.last_update = self.current_time()

        self.interval = interval
        self.lock = Lock()

    def _start(self):
        RepeatScheduler(self, self.interval).start()

    def update(self):
        self.last_update = self.current_time()

        with self.lock:
            for s in self.stocks:
                s.update()

    def add_stock(self, stock):
        self.stocks.append(stock)

    def current_time(self):
        return "{0:%Y-%m-%d %H:%M:%S}".format(datetime.now())

    @property
    def data(self):
        data = {}
        with self.lock:
            for s in self.stocks:
                price = f"{s.price:.05f}"
                data[s.symbol] = dict(price=price, datetime=self.last_update)
        return data


class SimulatedStock:
    def __init__(self, symbol, start_price, lo, hi, step=None, rise=True):
        self.symbol = symbol
        self.price = start_price
        self.lo = lo
        self.hi = hi
        assert self.is_within_bounds(self.price)

        self.rise = rise
        self.step = (hi - lo) / 100 if step is None else step

    def update(self):
        delta = 1 if self.rise else -1
        delta *= self.step

        if self.is_within_bounds(self.price + delta):
            self.price += delta

        elif self.is_within_bounds(self.price - delta):
            self.rise = not self.rise
            self.price -= delta

    def is_within_bounds(self, price):
        return self.lo <= price and price <= self.hi


POLL_AT_SECOND = 15


def seconds_until_next_minute():
    return 60 + POLL_AT_SECOND - datetime.now().second


class RepeatScheduler(Thread):
    def __init__(self, provider, wait_for_x_seconds):
        super().__init__()
        self.daemon = True
        self.provider = provider
        self.wait_for_x_seconds = wait_for_x_seconds

    def run(self):
        while True:
            self.provider.update()

            if callable(self.wait_for_x_seconds):
                x = self.wait_for_x_seconds()
            else:
                x = self.wait_for_x_seconds

            time.sleep(x)