from src.real_time_market_data.repeated_update_provider import RepeatedUpdateProvider, seconds_until_next_minute
from twelvedata import TDClient


class TDProvider(RepeatedUpdateProvider):
    def __init__(self, api_key, **kwargs):
        super().__init__(**kwargs, repeat_in_x_seconds=seconds_until_next_minute)

        self.td = TDClient(api_key=api_key)
        self.symbols_and_exchanges = [f"{symbol:exchange}" for symbol, exchange in self.symbol_to_exchange.items()]

    def get_init_data(self):
        # TODO change from days to specifying start time
        return self.make_request(days=365)

    def get_update_data(self):
        return self.make_request(days=2)

    def make_request(self, days):
        msg = self.td.time_series(
            symbol=self.symbols_and_exchanges,
            interval="1day",
            outputsize=days,
            timezone="Australia/Sydney",  # output all timestamps in Sydney's timezone TODO verify if this is desirable
        ).as_json()

        if len(self.symbols) == 1:
            return {self.symbols[0]: msg}

        return {self.without_exchange(symbol_and_exchange): data for symbol_and_exchange, data in msg}

    def without_exchange(self, symbol_and_exchange):
        return symbol_and_exchange.split(":")[0]
