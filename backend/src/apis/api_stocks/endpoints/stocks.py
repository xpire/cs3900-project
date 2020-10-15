from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import json, os
import requests
import numpy as np

from backend.src.core.config import settings

router = APIRouter()

# Start implementation here, this file handles batch and single stock data retrieval

# Can change to a different structure later

API_URL = "https://api.twelvedata.com"
API_KEY = settings.TD_API_KEY

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
