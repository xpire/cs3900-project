


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
