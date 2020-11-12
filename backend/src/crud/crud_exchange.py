"""
Mimicks a database and gives stock exchange objects for opening/closing times
"""

from datetime import timedelta
from typing import List, Optional

from src.domain_models.data_provider.setup import exchange_info
from src.schemas.exchange import Exchange

# Trading hours retrieved from https://www.thebalance.com/stock-market-hours-4773216
delta = lambda hours, minutes=0: timedelta(hours=hours, minutes=minutes)
exchanges = dict(
    ASX=Exchange(name="ASX", open=delta(10), close=delta(16), timezone="Australia/Sydney"),
    NYSE=Exchange(name="NYSE", open=delta(9, 30), close=delta(16), timezone="America/New_York"),
    NASDAQ=Exchange(name="NASDAQ", open=delta(9, 30), close=delta(16), timezone="America/New_York"),
    LSE=Exchange(name="LSE", open=delta(8), close=delta(16, 30), timezone="Europe/London"),
    **exchange_info
)


class CRUDExchange:
    def get_all_exchanges(self) -> List[Exchange]:
        return list(exchanges.values())

    def get_exchange_by_name(self, name) -> Optional[Exchange]:
        return exchanges.get(name, None)


exchange = CRUDExchange()
