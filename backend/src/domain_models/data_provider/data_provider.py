"""
Provides necessary stock information to functions through out the code base
"""

from abc import ABC, abstractmethod, abstractproperty


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
    # Direct getters for cached data
    # #
    def get_curr_day_close(self, symbol):
        return self.data[symbol]["curr_day_close"]

    def get_curr_day_open(self, symbol):
        return self.data[symbol]["curr_day_open"]

    def get_prev_day_close(self, symbol):
        return self.data[symbol]["prev_day_close"]

    def curr_price(self, symbol):
        return self.get_curr_day_close(symbol)
