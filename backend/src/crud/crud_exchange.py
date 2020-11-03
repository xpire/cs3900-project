from datetime import timedelta
from typing import List, Optional

from src.schemas.exchange import ExchangeFromDB

# Trading hours retrieved from https://www.thebalance.com/stock-market-hours-4773216
# TODO migrate to db

delta = lambda hours, minutes=0: timedelta(hours=hours, minutes=minutes)
exchanges = dict(
    ASX=ExchangeFromDB(name="ASX", open=delta(10), close=delta(16), timezone="Australia/Sydney"),
    NYSE=ExchangeFromDB(name="NYSE", open=delta(9, 30), close=delta(16), timezone="America/New_York"),
    NASDAQ=ExchangeFromDB(name="NASDAQ", open=delta(9, 30), close=delta(16), timezone="America/New_York"),
    LSE=ExchangeFromDB(name="LSE", open=delta(8), close=delta(16, 30), timezone="Europe/London"),
    XD00=ExchangeFromDB(name="XD00", open=delta(0), close=delta(6), timezone="Australia/Sydney", simulated=True),
    XD06=ExchangeFromDB(name="XD06", open=delta(6), close=delta(12), timezone="Australia/Sydney", simulated=True),
    XD12=ExchangeFromDB(name="XD12", open=delta(12), close=delta(18), timezone="Australia/Sydney", simulated=True),
    XD18=ExchangeFromDB(name="XD18", open=delta(18), close=delta(24), timezone="Australia/Sydney", simulated=True),
)


class CRUDExchange:
    def get_all_exchanges(self) -> List[ExchangeFromDB]:
        return list(exchanges.values())

    def get_exchange_by_name(self, name) -> Optional[ExchangeFromDB]:
        return exchanges.get(name, None)


exchange = CRUDExchange()
