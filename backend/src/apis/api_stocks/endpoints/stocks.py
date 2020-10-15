import json
import os
from typing import Any, List

import numpy as np
import requests
from backend.src.core.config import settings
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.real_time_market_data.data_provider import (
    CompositeDataProvider,
    RealTimeDataProvider,
    SimulatedDataProvider,
    SimulatedStock,
)

API_URL = "https://api.twelvedata.com"
API_KEY = settings.TD_API_KEY

provider1 = RealTimeDataProvider(
    symbols=["WOW:ASX", "ADES:LSE", "ACC:NSE", "AAPL"],
    apikey=API_KEY,
)

stocks = [
    SimulatedStock("SIM-1", 100, 10, 200),
    SimulatedStock("SIM-2", 150, 50, 1000, rise=False),
    SimulatedStock("SIM-3", 400, 20, 500),
]
provider2 = SimulatedDataProvider(stocks)
data_provider = CompositeDataProvider([provider1, provider2])
data_provider.start()

router = APIRouter()


@router.get("/real_time")
def get_real_time_data():
    return data_provider.data


# Start implementation here, this file handles batch and single stock data retrieval

# Can change to a different structure later

STOCKS = {}
with open("stocks.json") as json_file:
    STOCKS = json.load(json_file)

# -------------------------------
# For now, return hardcoded data
# -------------------------------


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
        if symbol not in STOCKS:
            raise HTTPException(status_code=404, detail="Item not found")

        # TODO: Popoulate with actual data
        ret.append(
            {
                "symbol": symbol,
                "exchange": STOCKS[symbol],
                "day_gain": np.random.randint(20) - 10,
                "latest_price": np.random.randint(1000),
            }
        )

    return ret


@router.get("/stocks/time_series")
async def get_stock_data(symbol: str = Query(None), days: int = 90):
    ret = []

    r = requests.get(
        f"{API_URL}/time_series?symbol={symbol}&interval=1day&apikey={API_KEY}&outputsize={days}"
    )

    return r.json()["values"]
