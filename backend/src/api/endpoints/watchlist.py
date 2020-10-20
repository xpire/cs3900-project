from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api.deps import check_symbol, decode_token, get_current_user_m, get_db
from src.core.config import settings
from src.core.watchlist import check_exists_watchlist
from src.db.session import SessionLocal

router = APIRouter()


@router.get("")
async def get_watchlist(
    user: models.User = Depends(get_current_user_m), db: Session = Depends(get_db)
):
    ret = []
    for entry in user.watchlist:
        ret += [
            {
                "name": entry.stock.name,
                "symbol": entry.stock.symbol,
                "exchange": entry.stock.exchange,
            }
        ]

    return ret


@router.post("")
async def update_watchlist(
    symbol: str = Depends(check_symbol),
    user: models.User = Depends(get_current_user_m),
    db: Session = Depends(get_db),
):
    # Check if already exists
    if check_exists_watchlist(user, symbol):
        return {"result": "symbol already exists"}

    crud.user.add_to_watch_list(db, user, symbol)

    return {"result": "success"}


@router.delete("")
async def delete_watchlist(
    symbol: str = Depends(check_symbol),
    user: models.User = Depends(get_current_user_m),
    db: Session = Depends(get_db),
):
    # Check if already exists
    if not check_exists_watchlist(user, symbol):
        return {"result": "symbol does not exist in watchlist"}

    crud.user.delete_from_watch_list(db, user, symbol)

    return {"result": "success"}
