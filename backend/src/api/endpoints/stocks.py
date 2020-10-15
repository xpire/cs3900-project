import json
import numpy as np
import os
from typing import Any, List


from src.core.config import settings
from src import crud
from src.api.deps import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from twelvedata import TDClient

from src.real_time_market_data.data_provider import (
    CompositeDataProvider,
    RealTimeDataProvider,
    SimulatedDataProvider,
    SimulatedStock,
    LatestClosingPriceProvider,
)

API_URL = "https://api.twelvedata.com"
API_KEY = "a603f4e94a3f4ebc8116636cd8e6aaba"  # settings.TD_API_KEY

router = APIRouter()


# Start implementation here, this file handles batch and single stock data retrieval
# Can change to a different structure later

STOCKS = {}
with open("stocks.json") as json_file:
    STOCKS = json.load(json_file)

# -------------------------------
# For now, return hardcoded data
# -------------------------------

TD = TDClient(apikey=API_KEY)

stock_names = [f"{symbol}:{exchange}" for symbol, exchange in STOCKS.items()]
data_provider = RealTimeDataProvider(
    symbols=stock_names,
    apikey=API_KEY,
)
latest_close_price_provider = LatestClosingPriceProvider(
    symbols=stock_names,
    apikey=API_KEY,
)
data_provider.start()
latest_close_price_provider.start()


@router.get("/real_time")
def get_real_time_data():
    return data_provider.data


@router.get("/real_times")
def get_real_time_data(symbol: str):
    return data_provider.data[symbol]


@router.get("/symbols")
async def get_symbols():
    ret = []
    for symbol in STOCKS:
        ret.append({"symbol": symbol, "exchange": STOCKS[symbol]})
    return ret


@router.get("/stocks")
async def get_stocks(symbols: List[str] = Query(None), db: Session = Depends(get_db)):
    ret = []

    # Can make for efficient later
    for symbol in symbols:
        stock = crud.stock.get_stock_by_symbol(db, symbol)
        if stock is None:
            raise HTTPException(status_code=404, detail="Item not found")

        ret.append(
            dict(
                symbol=symbol,
                name=stock.full_name,
                exchange=stock.exchange,
                curr_close_price=float(latest_close_price_provider.data[symbol][0]),
                prev_close_price=float(latest_close_price_provider.data[symbol][1]),
            )
        )
    return ret


@router.get("/time_series")
async def get_stock_data(symbol: str = Query(None), days: int = 90):
    data = TD.time_series(
        symbol=f"{symbol}:{STOCKS[symbol]}",
        interval="1day",
        outputsize=days, # TODO there seems to be a bug
        timezone="Australia/Sydney",
    ).as_json()
    return data
