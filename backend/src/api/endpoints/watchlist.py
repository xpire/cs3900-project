from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import crud, domain_models, models, schemas
from src.api.deps import check_symbol, get_current_user_dm, get_current_user_m, get_db
from src.core.config import settings
from src.db.session import SessionLocal
from src.schemas.response import Response

router = APIRouter()


@router.get("")
async def get_watchlist(user: models.User = Depends(get_current_user_m), db: Session = Depends(get_db)):
    ret = []
    for entry in user.watchlist:
        ret += [
            {
                "name": entry.stock_info.name,
                "symbol": entry.stock_info.symbol,
                "exchange": entry.stock_info.exchange,
            }
        ]

    return ret


@router.post("")
async def update_watchlist(
    symbol: str = Depends(check_symbol),
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    # Check if already exists
    if user.check_exists_watchlist(symbol):
        raise HTTPException(status_code=400, detail=f"Symbol {symbol} already exists in watchlist.")

    crud.user.add_to_watch_list(db, user.model, symbol)

    return Response(f"{symbol} added to watchlist")


@router.delete("")
async def delete_watchlist(
    symbol: str = Depends(check_symbol),
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    # Check if already exists
    if not user.check_exists_watchlist(symbol):
        raise HTTPException(status_code=400, detail=f"Symbol {symbol} does not exist in watchlist.")

    crud.user.delete_from_watch_list(db, user.model, symbol)

    return Response(f"{symbol} removed from watchlist")
