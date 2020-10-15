import json
import os
from typing import Any, List

import numpy as np
import json, os

from backend.src.core.config import settings
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

STOCK_INFO = {}
for symbol, exchange in STOCKS.items():
    info = TD.get_stocks_list(symbol=symbol, exchange=exchange).as_json()
    for data in info:
        if data["symbol"] == symbol:
            STOCK_INFO[symbol] = data
            break

print(STOCK_INFO)


# CURRENTLY USELESS
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
async def get_stocks(symbols: List[str] = Query(None)):
    ret = []

    # Can make for efficient later
    for symbol in symbols:
        if symbol not in STOCK_INFO:
            raise HTTPException(status_code=404, detail="Item not found")

        data = latest_close_price_provider.data[symbol]
        info = STOCK_INFO[symbol]
        info["last_close_price"] = float(data)
        ret.append(info)
    return ret


@router.get("/stocks/time_series")
async def get_stock_data(symbol: str = Query(None), days: int = 90):
    return TD.time_series(
        symbol=symbol,
        interval="1day",
        outputsize=str(days),
        timezone="Australia/Sydney",
    ).as_json()
