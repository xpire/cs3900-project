from typing import Any, List

import numpy as np
import src.api.endpoints.stocks as stocks_api
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api.deps import decode_token, get_current_user_m, get_db
from src.api.endpoints.stocks import latest_close_price_provider
from src.core.config import settings
from src.db.session import SessionLocal

router = APIRouter()


@router.get("")
async def get_portfolio(user: models.User = Depends(get_current_user_m), db: Session = Depends(get_db)):

    ret = {}
    ret["balance"] = user.balance
    ret["portfolio"] = []

    total_value = 0
    for stock in stocks_api.STOCKS:
        entry = {}

        entry["price"] = float(stocks_api.latest_close_price_provider.data[stock.symbol][0])
        entry["previous_price"] = float(stocks_api.latest_close_price_provider.data[stock.symbol][1])

        entry["symbol"] = stock.symbol
        entry["name"] = stock.name

        # Temporary data, change to actual data in database when implemented
        entry["owned"] = np.random.randint(20)
        entry["average_paid"] = entry["price"] + (10 - np.random.randint(20)) * entry["price"] / 100
        entry["total_paid"] = entry["average_paid"] * entry["owned"]
        entry["value"] = entry["price"] * entry["owned"]
        entry["gain"] = entry["value"] - entry["total_paid"]
        entry["day_gain"] = entry["price"] - entry["previous_price"]
        entry["return"] = entry["gain"] / entry["total_paid"]

        total_value += entry["value"]

        ret["portfolio"] += [entry]

    ret["total_value"] = total_value

    return ret
