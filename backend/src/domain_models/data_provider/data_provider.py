from abc import ABC, abstractmethod, abstractproperty

"""
TODO
- how to test limit order execution etc.
- limit order test: don't use latest data, but use lo and high since we get data
in blocks of 5
- confirmation message: Executed at ... / indicate positions on the stock?
- after you trade, we want to see immediate changes to the balance, networth, short/long networths,
and portfolio
- portfolio - inventory system: hover to see more details, click for even more
- floaty + button?
"""


class DataProvider(ABC):
    """
    Retrieves stock data and provides direct access to cached data
    """

    def __init__(self):
        self.is_running = False
        self.callbacks = []

    def pre_start(self):
        """
        To execute before calling start()
        """
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

    def subscribe(self, callback):
        """
        Subscribe [observer] to regular updates
        """
        callback()
        self.callbacks.append(callback)

    def notify(self):
        """
        Notify all observers through callbacks
        """
        for callback in self.callbacks:
            callback()

    @property
    def data(self):
        """
        Return cached data
        """
        return self.data_with_id[0]

    @abstractproperty
    def data_with_id(self):
        """
        Return cached data with an id that is updated whenver the data is changed (for caching purposes)
        """
        pass

    @abstractproperty
    def symbols(self):
        pass

    # #
    # Direct gettors for cached data
    # #
    def get_curr_day_close(self, symbol):
        return self.data[symbol]["curr_day_close"]

    def get_curr_day_open(self, symbol):
        return self.data[symbol]["curr_day_open"]

    def get_prev_day_close(self, symbol):
        return self.data[symbol]["prev_day_close"]

    def curr_price(self, symbol):
        return self.get_curr_day_close(symbol)
