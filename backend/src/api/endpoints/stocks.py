from datetime import datetime, time
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import crud
from src import domain_models as dm
from src import schemas
from src.api.deps import check_symbol, get_db
from src.core.config import settings
from src.core.utilities import HTTP400, log_msg
from src.db.session import SessionLocal
from src.domain_models.trading_hours import trading_hours_manager
from src.game.stat_update_publisher import StatUpdatePublisher
from src.real_time_market_data.composite_data_provider import CompositeDataProvider
from src.real_time_market_data.setup import create_simulators
from src.real_time_market_data.simulated_data_provider import SimulatedProvider
from src.real_time_market_data.td_data_provider import TDProvider
from src.schemas.response import Fail, Response, Success, return_response, return_result
from src.schemas.stock import StockAPIout
from twelvedata import TDClient

API_URL = "https://api.twelvedata.com"
API_KEY = settings.TD_API_KEY

router = APIRouter()


# Start implementation here, this file handles batch and single stock data retrieval
# Can change to a different structure later

# Retrieve all stocks
TD = TDClient(apikey=API_KEY)
market_data_provider = None

# TODO move this to a separate place
# We can't use deps to get the database here, on_event is not part of FastAPI so it can't use depends apparently
# https://github.com/tiangolo/fastapi/issues/425
@router.on_event("startup")
def startup_event():
    global market_data_provider

    db = SessionLocal()
    real_stocks = crud.stock.get_all_stocks(db=db, simulated=False)
    sim_stocks = crud.stock.get_all_stocks(db=db, simulated=True)

    def make_symbol_to_exchange(stocks):
        return {stock.symbol: stock.exchange for stock in stocks}

    # p1 = TDProvider(db=db, symbol_to_exchange=make_symbol_to_exchange(real_stocks), api_key=API_KEY)
    p2 = SimulatedProvider(
        db=db, symbol_to_exchange=make_symbol_to_exchange(sim_stocks), simulators=create_simulators(db)
    )
    market_data_provider = CompositeDataProvider([p2])  # p1
    market_data_provider.pre_start()
    market_data_provider.start()
    market_data_provider.subscribe(StatUpdatePublisher(db).update)
    market_data_provider.subscribe(dm.PendingOrderExecutor(db).update)


# TODO rename: /stocks
@router.get("/symbols")
async def get_symbols(db: Session = Depends(get_db)) -> List[StockAPIout]:
    return crud.stock.get_multi_by_symbols(db=db, symbols=market_data_provider.symbols)


# TODO rename: /real_time
@router.get("/stocks")
async def get_stocks(
    symbols: List[str] = Query(None), db: Session = Depends(get_db)
) -> List[schemas.StockRealTimeAPIout]:
    if not symbols:
        return []

    stocks = crud.stock.get_multi_by_symbols(db=db, symbols=symbols)
    if len(stocks) != len(symbols):
        Fail(f"Following symbols are requested but do not exist: {set(symbols) - set(stocks)}").assert_ok()

    ret = []
    for stock in stocks:
        ret.append(
            schemas.StockRealTimeAPIout(
                **stock.dict(),
                **market_data_provider.data[stock.symbol],
                trading_hours_info=trading_hours_manager.get_trading_hours_info(stock),
            )
        )
    return ret


@router.get("/time_series")
async def get_stock_data(
    symbol: str = Depends(check_symbol), db: Session = Depends(get_db), days: int = 90
) -> List[schemas.TimeSeriesAPIout]:
    return crud.stock.get_time_series(db=db, symbol=symbol, days=days)


@router.get("/trading_hours")
async def get_trading_hours(symbol: str = Depends(check_symbol), db: Session = Depends(get_db)):  # TODO define schema
    stock = crud.stock.get_by_symbol(db=db, symbol=symbol)
    return trading_hours_manager.get_trading_hours_info(stock)
