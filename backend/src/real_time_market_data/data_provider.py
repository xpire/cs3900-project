import datetime as dt
import itertools as it
import time
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
from threading import Lock, Thread

from src import crud
from src.schemas.time_series import TimeSeriesCreate
from twelvedata import TDClient

"""
TODO

BRING BACK THE SIMULATED DATA
- edit stocks.csv, with exchange name XD-00, XD-06, XD-12, XD-18 (timezones)
- bring back the simulated data provider, etc.
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
    def __init__(self, db, symbols):
        self.db = db
        self.is_running = False
        self.observers = []

        self.symbols = symbols
        self.db = db

        self._data = {}
        self.lock = Lock()

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.init_data()
            self._start()

    @abstractmethod
    def _start(self):
        pass

    @abstractmethod
    def pre_init_data(self):
        pass

    def init_data(self):
        msg = self.get_init_data()
        print("===== INITIALISING MARKET DATA =====")
        for symbol, data in msg.items():
            print(f"Number of entries for {symbol}: {len(data)}")
            crud.stock.batch_add_daily_time_series(db=self.db, stock_in=self.get_stock(symbol), time_series_in=data)
        print("===== FINISHED INITIALISATION =====")
        self.cache_latest_data(msg)

    @abstractmethod
    def get_init_data(self):
        pass

    def update(self):
        msg = self.get_update_data()
        for symbol, data in msg.items():
            crud.stock.update_time_series(db=self.db, stock_in=self.get_stock(symbol), u_time_series=data)
        self.cache_latest_data(msg)

        for observer in self.observers:
            observer.update(self.data)  # remove this parameter

    @abstractmethod
    def get_update_data(self):
        pass

    def subscribe(self, observer):
        self.observers.append(observer)

    def subscribe_with_update(self, observer):
        observer.update(self.data)  # remove this too
        self.observers.append(observer)

    def get_curr_day_close(self, symbol):
        return self.data[symbol]["curr_day_close"]

    def get_curr_day_open(self, symbol):
        return self.data[symbol]["curr_day_open"]

    def get_prev_day_close(self, symbol):
        return self.data[symbol]["prev_day_close"]

    def close(self):
        self.db.close()

    # figure this out
    def without_exchange(self, symbol):
        return symbol.split(":")[0]

    def get_stock(self, symbol):
        return crud.stock.get_stock_by_symbol(db=self.db, stock_symbol=self.without_exchange(symbol))

    def cache_latest_data(self, msg):
        temp = {**self._data}
        for symbol, data in msg.items():
            symbol = self.without_exchange(symbol)
            temp[symbol] = dict(
                curr_day_open=float(data[0]["open"]),
                curr_day_close=float(data[0]["close"]),
                prev_day_close=float(data[1]["close"]),
            )

        # switch out referneces
        with self.lock:
            self._data = temp

    @property
    def data(self):
        with self.lock:
            return self._data


class CompositeDataProvider(DataProvider):
    def __init__(self, providers, **kwargs):
        super().__init__()
        self.providers = providers

    def _start(self):
        for p in self.providers:
            p.start()

    def pre_init_data(self):
        for p in self.providers:
            p.pre_init_data()

    def get_init_data(self):
        data = {}
        for p in self.providers:
            data.extend(p.get_init_data())
        return data

    # TODO updates not synced
    # def get_update_data(self):
    #     data = {}
    #     for p in self.providers:
    #         data.extend(p.get_update_data())
    #     return data

    # @property
    # def data(self):
    #     data = {}
    #     for p in self.providers:
    #         data = {**data, **p.data} #TODO use extend instead for efficiency?
    #     return data


class MarketDataProvider(DataProvider):
    def __init__(self, apikey, symbols, db):
        super().__init__()

        self.TD = TDClient(apikey=apikey)

    def _start(self):
        RepeatScheduler(self, seconds_until_next_minute).start()

    def get_init_data(self):
        # change from days to specifying start time
        return self.make_request(days=365)

    def get_update_data(self):
        return self.make_request(days=2)

    def make_request(self, days):
        msg = self.TD.time_series(
            symbol=self.symbols,
            interval="1day",
            outputsize=days,
            timezone="Australia/Sydney",  # output all timestamps in Sydney's timezone
        ).as_json()

        if len(self.symbols) == 1:
            return {self.symbols[0]: msg}

        return msg


class SimulatedDataProvider(DataProvider):
    def __init__(self, stocks, interval=10):
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

    def get_init_data(self):
        # specify timezone
        msg = {}
        for s in self.stocks:
            msg[s.symbol] = s.make_request()
        return msg

    def get_update_date(self):
        # specify timezone
        msg = {}
        for s in self.stocks:
            msg[s.symbol] = s.make_request_by_days()
        return msg

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
