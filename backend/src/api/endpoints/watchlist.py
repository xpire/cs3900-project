from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api.deps import decode_token, get_current_user, get_db
from src.core.config import settings
from src.db.session import SessionLocal

router = APIRouter()


@router.get("")
async def get_watchlist(
    user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    ret = []
    for entry in user.watchlist:
        ret += [{"symbol": entry.symbol}]

    return ret


@router.post("")
async def update_watchlist(
    symbol: str, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    crud.user.add_to_watch_list(db, user, symbol)


@router.delete("")
async def delete_watchlist(
    symbol: str, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    crud.user.delete_from_watch_list(db, user, symbol)
