import datetime as dt
import itertools as it
import time
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
from threading import Lock, Thread
from typing import Tuple

from src import crud
from src.schemas.time_series import TimeSeriesCreate
from twelvedata import TDClient

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


class CompositeDataProvider(DataProvider):
    def __init__(self, providers, **kwargs):
        super().__init__(**kwargs)
        self.providers = providers
        self.last_ids = []
        self._data = {}
        self.id = 0

        for p in providers:
            p.subscribe(self.notify)

    def pre_start(self):
        for p in self.providers:
            p.pre_start()

    def on_start(self):
        for p in self.providers:
            p.start()

    def get_init_data(self):
        data = {}
        for p in self.providers:
            data.extend(p.get_init_data())
        return data

    @property
    def data_with_id(self):
        updated = False
        for p, last_id in zip(self.providers, self.last_ids):
            data, id = p.data_with_id

            if id != last_id:
                updated = True
                self._data.update(data)

        if updated:
            self.id += 1
        return (self._data, self.id)


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


class TDProvider(RepeatedPollingProvider):
    def __init__(self, apikey, **kwargs):
        super().__init__(**kwargs)

        self.TD = TDClient(apikey=apikey)
        self.symbols_and_exchanges = [f"{symbol:exchange}" for symbol, exchange in self.symbol_to_exchange.items()]

    def on_start(self):
        super().on_start()
        RepeatScheduler(self, seconds_until_next_minute).start()

    def get_init_data(self):
        # TODO change from days to specifying start time
        return self.make_request(days=365)

    def get_update_data(self):
        return self.make_request(days=2)

    def make_request(self, days):
        msg = self.TD.time_series(
            symbol=self.symbols_and_exchanges,
            interval="1day",
            outputsize=days,
            timezone="Australia/Sydney",  # output all timestamps in Sydney's timezone
        ).as_json()

        if len(self.symbols) == 1:
            return {self.symbols[0]: msg}

        return {self.without_exchange(symbol_and_exchange): data for symbol_and_exchange, data in msg}

    def without_exchange(self, symbol_and_exchange):
        return symbol_and_exchange.split(":")[0]


class SimulatedProvider(RepeatedPollingProvider):
    def __init__(self, stocks, interval=10):
        super().__init__()

        self.stocks = stocks
        self.interval = interval
        self.lock = Lock()

    def on_start(self):
        super().on_start()
        RepeatScheduler(self, self.interval).start()

    def get_init_data(self):
        # specify timezone
        msg = {}
        for s in self.stocks:
            msg[s.symbol] = s.make_request()  # TODO fill-in
        return msg

    def get_update_data(self):
        # specify timezone
        msg = {}
        for s in self.stocks:
            msg[s.symbol] = s.make_request_by_days()  # TODO fill-in
        return msg


trading_hours_manager = None


class SimulatedStock:
    def __init__(self, symbol, exchange, day_lo, day_hi, start_date=None, rise_at_start=True, volume=1000):
        self.symbol = symbol
        self.exchange = exchange
        self.day_lo = day_lo
        self.day_hi = day_hi
        self.start_date = start_date or dt.datetime(2019, 10, 1)
        self.rise_at_start = rise_at_start
        self.volume = volume
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
        info = trading_hours_manager.info(self.exchange)
        start, end = info["start"], info["end"]

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
        if (date - self.earliest_date).days % 2 == 0:
            return self.rise_at_start
        return not self.rise_at_start


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
