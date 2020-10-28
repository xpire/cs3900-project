from threading import Lock

from src.real_time_market_data.repeated_update_provider import RepeatedUpdateProvider


class SimulatedProvider(RepeatedUpdateProvider):
    def __init__(self, stocks, repeat_in_x_seconds=10, **kwargs):
        super().__init__(**kwargs, repeat_in_x_seconds=repeat_in_x_seconds)

        self.stocks = stocks
        self.lock = Lock()

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
