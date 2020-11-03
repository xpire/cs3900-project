import itertools as it
from functools import lru_cache

import numpy as np
from src import crud

from .composite_data_provider import CompositeDataProvider
from .simulated_data_provider import SimulatedProvider
from .simulated_stock import StockSimulator
from .td_data_provider import TDProvider

patterns = [
    list(200 + 100 * np.sin(np.linspace(-np.pi, np.pi - np.pi / 14, 27))),
    list(200 - 100 * np.sin(np.linspace(-np.pi, np.pi - np.pi / 14, 27))),
    list(it.chain(range(100, 600, 50), range(600, 100, -100))),
]

stock_details = dict(
    sim00=patterns[0],
    sim01=patterns[1],
    sim02=patterns[2],
    sim10=patterns[0],
    sim11=patterns[1],
    sim12=patterns[2],
    sim20=patterns[0],
    sim21=patterns[1],
    sim22=patterns[2],
    sim30=patterns[0],
    sim31=patterns[1],
    sim32=patterns[2],
)


def create_simulators(db):
    global stock_details

    simulators = []
    for symbol, day_patterns in stock_details.items():
        stock = crud.stock.get_by_symbol(db=db, symbol=symbol)
        simulators.append(StockSimulator(stock, day_patterns))
    return simulators


@lru_cache(maxsize=None)
def get_data_provider():
    from src import domain_models as dm
    from src.db.session import SessionLocal
    from src.game.stat_update_publisher import StatUpdatePublisher

    db = SessionLocal()

    real_stocks = crud.stock.get_all_stocks(db=db, simulated=False)
    sim_stocks = crud.stock.get_all_stocks(db=db, simulated=True)

    def make_symbol_to_exchange(stocks):
        return {stock.symbol: stock.exchange for stock in stocks}

    # p1 = TDProvider(db=db, symbol_to_exchange=make_symbol_to_exchange(real_stocks), api_key=settings.TD_API_KEY)
    p2 = SimulatedProvider(
        db=db, symbol_to_exchange=make_symbol_to_exchange(sim_stocks), simulators=create_simulators(db)
    )

    provider = CompositeDataProvider([p2])  # p1
    provider.pre_start()
    provider.start()
    provider.subscribe(StatUpdatePublisher(db).update)
    provider.subscribe(dm.PendingOrderExecutor(db).update)
    return provider
