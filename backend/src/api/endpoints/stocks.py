import json
import os
from datetime import datetime, time
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import crud
from src.api.deps import check_symbol, get_db
from src.core.config import settings
from src.core.utilities import fail_save, log_msg
from src.crud.crud_stock import stock
from src.db.session import SessionLocal
from src.real_time_market_data.data_provider import (
    CompositeDataProvider,
    LatestClosingPriceProvider,
    RealTimeDataProvider,
    SimulatedDataProvider,
    SimulatedStock,
)
from twelvedata import TDClient

API_URL = "https://api.twelvedata.com"
API_KEY = settings.TD_API_KEY

router = APIRouter()


# Start implementation here, this file handles batch and single stock data retrieval
# Can change to a different structure later

# Retrieve all stocks
STOCKS = []

TD = TDClient(apikey=API_KEY)


# data_provider = RealTimeDataProvider(
#     symbols=stock_names,
#     apikey=API_KEY,
# )
latest_close_price_provider = None
# data_provider.start()


# We can't use deps to get the database here, on_event is not part of FastAPI so it can't use depends apparently
# https://github.com/tiangolo/fastapi/issues/425
@router.on_event("startup")
def startup_event():
    global STOCKS
    global latest_close_price_provider

    db = SessionLocal()
    STOCKS = crud.stock.get_all_stocks(db=db)[:10]  # Change this slice later

    stock_names = [f"{stock.symbol}:{stock.exchange}" for stock in STOCKS]

    if stock_names:
        latest_close_price_provider = LatestClosingPriceProvider(
            symbols=stock_names, apikey=API_KEY, db=db, crud_obj=stock
        )
        latest_close_price_provider.start()
    else:
        log_msg("There are no stocks in the database, not polling for data.", "WARNING")


@router.on_event("shutdown")
def startup_event():
    latest_close_price_provider.close()


# @router.get("/real_time")
# async def get_real_time_data():
#     return data_provider.data


# @router.get("/real_times")
# async def get_real_time_data(symbol: str):
#     return data_provider.data[symbol]


@router.get("/symbols")
async def get_symbols(db: Session = Depends(get_db)):
    ret = []

    for stock in STOCKS:
        ret.append(
            {
                "symbol": stock.symbol,
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
        stock = crud.stock.get_stock_by_symbol(db, symbol)
        if stock is None:
            raise HTTPException(status_code=404, detail="Item not found")

        ret.append(
            dict(
                symbol=symbol,
                name=stock.name,
                exchange=stock.exchange,
                curr_close_price=float(latest_close_price_provider.data[symbol][0]),
                prev_close_price=float(latest_close_price_provider.data[symbol][1]),
                commission=0.005,
            )
        )
    return ret


@router.get("/time_series")
async def get_stock_data(symbol: str = Depends(check_symbol), db: Session = Depends(get_db), days: int = 90):
    stock = crud.stock.get_stock_by_symbol(db, symbol)

    data = crud.stock.get_time_series(db, stock)
    # data = TD.time_series(
    #     symbol=f"{stock.symbol}:{stock.exchange}",
    #     interval="1day",
    #     outputsize=days,  # TODO there seems to be a bug
    #     timezone="Australia/Sydney",
    # ).as_json()
    return data


@router.get("/trading_hours")
async def get_trading_hours(symbol: str = Depends(check_symbol), db: Session = Depends(get_db)):

    # Trading hours retrieved from
    # https://www.thebalance.com/stock-market-hours-4773216#:~:text=Toronto%20Stock%20Exchange-,9%3A30%20a.m.%20to%204%20p.m.,30%20p.m.%20to%209%20p.m.&text=8%3A30%20a.m.%20to%203%20p.m.

    stock = crud.stock.get_stock_by_symbol(db, symbol)
    curr_time = datetime.now().time()  # UTC time

    res = False
    time_range = None
    # Australian is 10am - 4pm (AEDT)
    if stock.exchange == "ASX":
        if curr_time >= time(23, 0) or curr_time <= time(5, 0):
            res = True
        time_range = f"{time(23,0)} - {time(5,0)}"
    if stock.exchange == "NYSE":  # NYSE is 9:30 am - 4 pm (New York Eastern time (UTC-4))
        if curr_time >= time(13, 30) and curr_time <= time(20, 0):
            res = True
        time_range = f"{time(13, 30)} - {time(20,0)}"
    if stock.exchange == "NASDAQ":  # NYSE is 9:30 am - 4 pm (New York Eastern time (UTC-4))
        if curr_time >= time(13, 30) and curr_time <= time(20, 0):
            res = True
        time_range = f"{time(13, 30)} - {time(20,0)}"
    if stock.exchange == "LSE":
        if curr_time >= time(8, 0) and curr_time <= time(16, 30):
            res = True
        time_range = f"{time(8, 0)} - {time(16, 30)}"

    return {"trading": res, "time_range": time_range}
