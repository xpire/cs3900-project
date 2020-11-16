"""
Methods to access necessary data for simulated stocks
"""

import datetime as dt

from .repeated_update_provider import RepeatedUpdateProvider


class SimulatedProvider(RepeatedUpdateProvider):
    def __init__(self, simulators, repeat_in_x_seconds=10, **kwargs):
        super().__init__(**kwargs, repeat_in_x_seconds=repeat_in_x_seconds)

        self.simulators = simulators

    def get_init_data(self):
        return self.get_data_by_days(365)

    def get_update_data(self):
        return self.get_data_by_days(2)

    def get_data_by_days(self, days):
        now = dt.datetime.now()

        msg = {}
        for s in self.simulators:
            msg[s.symbol] = s.make_request_by_days(now, days)
        return msg
