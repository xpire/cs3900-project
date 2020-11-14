"""
Common hub for all data providers to communicate through.
"""

from .data_provider import DataProvider


class CompositeDataProvider(DataProvider):
    def __init__(self, providers, **kwargs):
        super().__init__(**kwargs)
        self.providers = providers
        self.last_ids = [None] * len(providers)

        self._data = {}
        self.id = 0

        # relay all notifications from the providers to the subscribers
        for p in providers:
            p.subscribe(self.notify)

    def on_start(self):
        for p in self.providers:
            p.pre_start()

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
        for i, p in enumerate(self.providers):
            data, id = p.data_with_id

            if id != self.last_ids[i]:
                self.last_ids[i] = id
                self._data.update(data)
                updated = True

        if updated:
            self.id += 1

        return (self._data, self.id)

    @property
    def symbols(self):
        symbols = set()
        for p in self.providers:
            symbols.update(p.symbols)
        return symbols
