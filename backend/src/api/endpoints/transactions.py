from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import domain_models
from src.api.deps import check_symbol, get_current_user_dm, get_db
from src.core.config import settings
from src.db.session import SessionLocal

from src.schemas.response import Respons

router = APIRouter()


@router.get("")
async def get_transactions(
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
):
    ret = []

    for transaction in user.model.transaction_hist:
        ret += {
            "t_type": transaction.action,
            "symbol": transaction.symbol,
            "name": transaction.stock_info.name,
            "amount": transaction.amount,
            "price": transaction.price,
            "value": transaction.amount * transaction.price,
        }

    return ret
