import datetime as dt

from src.real_time_market_data.repeated_update_provider import (
    RepeatedUpdateProvider, seconds_until_next_minute)
from twelvedata import TDClient


class TDProvider(RepeatedUpdateProvider):
    def __init__(self, api_key, **kwargs):
        super().__init__(**kwargs, repeat_in_x_seconds=seconds_until_next_minute)

        self.td = TDClient(api_key=api_key)
        self.symbols_and_exchanges = [f"{symbol}:{exchange}" for symbol, exchange in self.symbol_to_exchange.items()]

    def get_init_data(self):
        now = dt.datetime.now()
        start_date = (now - dt.timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")

        request = self.td.time_series(
            symbol=self.symbols_and_exchanges,
            interval="1day",
            timezone="Australia/Sydney",  # TODO make config, and set datetime timezone using https://stackoverflow.com/questions/1301493/setting-timezone-in-python
            start_date=start_date,
        )
        return self.make_request(request)

    def get_update_data(self):
        request = self.td.time_series(
            symbol=self.symbols_and_exchanges,
            interval="1day",
            outputsize=2,
            timezone="Australia/Sydney",  # output all timestamps in Sydney's timezone TODO verify if this is desirable
        )
        return self.make_request(request)

    def make_request(self, request):
        msg = request.as_json()

        if len(self.symbols) == 1:
            return {self.symbols[0]: msg}

        return {self.without_exchange(symbol_and_exchange): data for symbol_and_exchange, data in msg}

    def without_exchange(self, symbol_and_exchange):
        return symbol_and_exchange.split(":")[0]
