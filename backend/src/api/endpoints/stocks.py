import json
import os
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import crud
from src.api.deps import get_db
from src.core.config import settings
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

    try:
        db = SessionLocal()
        STOCKS = crud.stock.get_all_stocks(db)[:10]  # Change this slice later
        print(len(crud.stock.get_all_stocks(db)))
        stock_names = [f"{stock.symbol}:{stock.exchange}" for stock in STOCKS]
        print(stock_names)

        latest_close_price_provider = LatestClosingPriceProvider(
            symbols=stock_names, apikey=API_KEY,
        )
        latest_close_price_provider.start()
    finally:
        db.close()


@router.get("/real_time")
async def get_real_time_data():
    return data_provider.data


@router.get("/real_times")
async def get_real_time_data(symbol: str):
    return data_provider.data[symbol]


@router.get("/symbols")
async def get_symbols(db: Session = Depends(get_db)):
    ret = []

    for stock in STOCKS:
        ret.append(
            {"symbol": stock.symbol, "exchange": stock.exchange,}
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
            )
        )
    return ret


@router.get("/time_series")
async def get_stock_data(symbol: str = Query(None), db: Session = Depends(get_db), days: int = 90):
    stock = crud.stock.get_stock_by_symbol(db, symbol)

    data = TD.time_series(
        symbol=f"{stoc.symbol}:{stock.exchange}",
        interval="1day",
        outputsize=days,  # TODO there seems to be a bug
        timezone="Australia/Sydney",
    ).as_json()
    return data
