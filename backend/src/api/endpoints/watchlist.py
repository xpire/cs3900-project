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
    pass


@router.post("")
async def update_watchlist(
    user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    pass


@router.delete("")
async def delete_watchlist(
    user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    pass
