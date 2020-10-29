from datetime import time
from typing import List, Optional

from pytz import timezone
from src.schemas.exchange import ExchangeFromDB

# Trading hours retrieved from https://www.thebalance.com/stock-market-hours-4773216
# TODO migrate to db
# exchange_info = dict(
#     ASX=dict(start=time(10, 0), end=time(16, 0), timezone=timezone("Australia/Sydney"), simulated=False),
#     NYSE=dict(start=time(9, 30), end=time(16, 0), timezone=timezone("America/New_York"), simulated=False),
#     NASDAQ=dict(start=time(9, 30), end=time(16, 0), timezone=timezone("America/New_York"), simulated=False),
#     LSE=dict(start=time(8, 0), end=time(16, 30), timezone=timezone("Europe/London"), simulated=False),
#     XD00=dict(start=time(0, 0), end=time(6, 0), timezone=timezone("Australia/Sydney"), simulated=True),
#     XD06=dict(start=time(6, 0), end=time(12, 0), timezone=timezone("Australia/Sydney"), simulated=True),
#     XD12=dict(start=time(12, 0), end=time(18, 0), timezone=timezone("Australia/Sydney"), simulated=True),
#     XD18=dict(start=time(18, 0), end=time(24, 0), timezone=timezone("Australia/Sydney"), simulated=True),
# )

exchanges = dict(
    ASX=ExchangeFromDB(name="ASX", start=time(10, 0), end=time(16, 0), timezone="Australia/Sydney"),
    NYSE=ExchangeFromDB(start=time(9, 30), end=time(16, 0), timezone="America/New_York"),
    NASDAQ=ExchangeFromDB(start=time(9, 30), end=time(16, 0), timezone="America/New_York"),
    LSE=ExchangeFromDB(start=time(8, 0), end=time(16, 30), timezone="Europe/London"),
    XD00=ExchangeFromDB(start=time(0, 0), end=time(6, 0), timezone="Australia/Sydney", simulated=True),
    XD06=ExchangeFromDB(start=time(6, 0), end=time(12, 0), timezone="Australia/Sydney", simulated=True),
    XD12=ExchangeFromDB(start=time(12, 0), end=time(18, 0), timezone="Australia/Sydney", simulated=True),
    XD18=ExchangeFromDB(start=time(18, 0), end=time(24, 0), timezone="Australia/Sydney", simulated=True),
)


class CRUDExchange:
    def get_all_exchanges(db) -> List[ExchangeFromDB]:
        return list(exchanges.values())

    def get_exchange_by_name(db, name) -> Optional[ExchangeFromDB]:
        return exchanges.get(name, None)


exchange = CRUDExchange()
