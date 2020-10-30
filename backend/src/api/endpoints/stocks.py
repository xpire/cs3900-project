from datetime import datetime, time
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import crud
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
    stocks = crud.stock.get_all_stocks(db=db)[:12]  # TODO change this slice later
    # symbols = [f"{stock.symbol}:{stock.exchange}" for stock in stocks]
    symbol_to_exchange = {stock.symbol: stock.exchange for stock in stocks}

    if symbol_to_exchange:
        # p1 = TDProvider(db=db, symbol_to_exchange=symbol_to_exchange, api_key=API_KEY)
        p2 = SimulatedProvider(db=db, symbol_to_exchange=symbol_to_exchange, simulators=create_simulators(db))
        market_data_provider = CompositeDataProvider([p2])  # p1
        market_data_provider.pre_start()
        market_data_provider.subscribe(StatUpdatePublisher(db).update)
        # TODO @Song, place the order execution below the above subscribe
        market_data_provider.start()
    else:
        log_msg("There are no stocks in the database, not polling for data.", "WARNING")


# @router.on_event("shutdown")
# def startup_event():
#     market_data_provider.close()


@router.get("/symbols")
async def get_symbols(db: Session = Depends(get_db)):
    ret = []

    stocks = crud.stock.get_all_stocks(db=db)[:12]
    for stock in stocks:
        ret.append(
            {
                "symbol": stock.symbol,
                "name": stock.name,
                "exchange": stock.exchange,
            }
        )

    return ret


@router.get("/stocks")
async def get_stocks(symbols: List[str] = Query(None), db: Session = Depends(get_db)):
    ret = []
    if not symbols:
        return ret

    # Can make for efficient later
    for symbol in symbols:
        stock = crud.stock.get_stock_by_symbol(db=db, stock_symbol=symbol)
        if stock is None:
            raise HTTPException(status_code=404, detail="Item not found")

        ret.append(
            dict(
                symbol=symbol,
                name=stock.name,
                exchange=stock.exchange,
                curr_close_price=market_data_provider.get_curr_day_close(symbol),
                prev_close_price=market_data_provider.get_prev_day_close(symbol),
                commission=0.005,  # TODO move to a config
                **trading_hours_manager.get_trading_hours_info(stock),
            )
        )
    return ret


@router.get("/time_series")  # TODO days param is not currently being used
async def get_stock_data(symbol: str = Depends(check_symbol), db: Session = Depends(get_db), days: int = 90):
    stock = crud.stock.get_stock_by_symbol(db=db, stock_symbol=symbol)
    return crud.stock.get_time_series(db=db, stock_in=stock)


# TODO change check_symbol to get_by_symbol
@router.get("/trading_hours")
async def get_trading_hours(symbol: str = Depends(check_symbol), db: Session = Depends(get_db)):
    stock = crud.stock.get_stock_by_symbol(db=db, stock_symbol=symbol)
    return trading_hours_manager.get_trading_hours_info(stock)
