from typing import Any, List

import numpy as np

import src.api.endpoints.stocks as stocks_api
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import crud, domain_models, schemas
from src.api.deps import decode_token, get_current_user_dm, get_db
from src.api.endpoints.stocks import latest_close_price_provider
from src.core.config import settings
from src.db.session import SessionLocal

router = APIRouter()


@router.get("")
async def get_portfolio(
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
):

    ret = {}
    ret["balance"] = user.model.balance
    ret["long"] = user.get_positions("long")
    ret["short"] = user.get_postions("short")

    return ret
