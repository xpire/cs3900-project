from typing import Any, List

import numpy as np
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api.deps import decode_token, get_current_user, get_db
from src.api.endpoints.stocks import STOCKS
from src.core.config import settings
from src.db.session import SessionLocal

router = APIRouter()


@router.get("")
async def get_portfolio(
    user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    ret = {}
    ret["balance"] = user.balance
    ret["portfolio"] = []

    for stock in STOCKS:
        temp = {}

        temp["symbol"] = stock.symbol
        temp["name"] = stock.name

        # Temporary data
        temp["price"] = np.random.randInt(1000)
        temp["owned"] = np.random.randInt(10)
        temp["average_paid"] = np.random.randInt(1000)
        temp["total_paid"] = np.random.randInt(1000)
