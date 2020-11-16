"""
This file communicates with twelvedata through its API to retrieve the necessary
stock data for our application.
Data retrieved includes:
    - historical daily prices
    - minute resolution updates to prices
    - stock information
Historical data is stored in our database, and minute updates are cached for quick acccess
without constant API calls
"""

import datetime as dt

from src.core.config import settings
from twelvedata import TDClient

from .repeated_update_provider import RepeatedUpdateProvider, seconds_until_next_minute


class TDProvider(RepeatedUpdateProvider):
    def __init__(self, api_key, **kwargs):
        super().__init__(**kwargs, repeat_in_x_seconds=seconds_until_next_minute)

        self.td = TDClient(apikey=api_key)
        self.symbols_and_exchanges = [f"{symbol}:{exchange}" for symbol, exchange in self.symbol_to_exchange.items()]

    def get_init_data(self):
        now = dt.datetime.now()
        start_date = (now - dt.timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")

        request = self.td.time_series(
            symbol=self.symbols_and_exchanges,
            interval="1day",
            timezone=settings.TIMEZONE,
            outputsize=365,
            start_date=start_date,
        )
        return self.make_request(request)

    def get_update_data(self):
        print("UPDATE TD PROVIDER")
        request = self.td.time_series(
            symbol=self.symbols_and_exchanges,
            interval="1day",
            outputsize=2,
            timezone=settings.TIMEZONE,  # output all timestamps in Sydney's timezone
        )
        return self.make_request(request)

    def make_request(self, request):
        msg = request.as_json()

        if len(self.symbols) == 1:
            return {self.symbols[0]: msg}

        return {self.without_exchange(symbol_and_exchange): data for symbol_and_exchange, data in msg.items()}

    def without_exchange(self, symbol_and_exchange):
        return symbol_and_exchange.split(":")[0]
