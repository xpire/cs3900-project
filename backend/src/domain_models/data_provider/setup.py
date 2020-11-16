"""
Setup file for our stock data
Includes both real market stocks through twelvedata and our own simulated stocks
Maintains TD API limits as well
"""

import itertools as it
from datetime import timedelta

from src import crud
from src.core.config import settings
from src.schemas.exchange import Exchange

from .composite_data_provider import CompositeDataProvider
from .simulated_data_provider import SimulatedProvider
from .simulated_stock import StockSimulator
from .td_data_provider import TDProvider

delta = lambda hours: timedelta(hours=hours)

patterns = [
    list(it.chain(range(2000, 100, -100), range(100, 2000, 100))),
    list(it.chain(range(100, 2000, 100), range(2000, 100, -100))),
]

stock_patterns = {}
exchange_info = {}

for i in range(24):
    symbol = f"sim{i:02.0f}"
    exchange = f"XD{i:02.0f}"
    stock_patterns[symbol + "a"] = patterns[0]
    stock_patterns[symbol + "b"] = patterns[1]
    exchange_info[exchange] = Exchange(
        name=exchange, open=delta(i), close=delta(i + 1), timezone=settings.TIMEZONE, simulated=True
    )


def create_simulators(db):
    global stock_patterns

    simulators = []
    for symbol, day_patterns in stock_patterns.items():
        stock = crud.stock.get_by_symbol(db=db, symbol=symbol)
        simulators.append(StockSimulator(stock, day_patterns))
    return simulators


def cached_get_data_provider():
    provider = None

    def get_data_provider():
        nonlocal provider
        if provider is not None:
            return provider

        from src import domain_models as dm
        from src.db.session import SessionLocal
        from src.game.stat_update_publisher import StatUpdatePublisher

        db = SessionLocal()

        real_stocks = crud.stock.get_all_stocks(db=db, simulated=False)[:50]
        sim_stocks = crud.stock.get_all_stocks(db=db, simulated=True)

        def make_symbol_to_exchange(stocks):
            return {stock.symbol: stock.exchange for stock in stocks}

        p1 = TDProvider(db=db, symbol_to_exchange=make_symbol_to_exchange(real_stocks), api_key=settings.TD_API_KEY)
        p2 = SimulatedProvider(
            db=db, symbol_to_exchange=make_symbol_to_exchange(sim_stocks), simulators=create_simulators(db)
        )

        provider = CompositeDataProvider([p1, p2])
        provider.pre_start()
        provider.start()
        provider.subscribe(StatUpdatePublisher().update)
        provider.subscribe(dm.PendingOrderExecutor().update)

        # Subscribe to TD data provider, tick every 1 minute
        p1.subscribe(dm.PortfolioWorthPublisher().update)

        return provider

    return get_data_provider


get_data_provider = cached_get_data_provider()
