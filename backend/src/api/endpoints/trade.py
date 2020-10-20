from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api.deps import check_symbol, decode_token, get_current_user_m, get_db
from src.core.config import settings
from src.db.session import SessionLocal

router = APIRouter()


@router.post("/market/buy")
async def market_buy(
    symbol: str = Depends(check_symbol),
    quantity: int,
    user: models.User = Depends(get_current_user_m),
    db: Session = Depends(get_db),
):

    return {"result": "success"}


@router.post("/market/sell")
async def market_sell(
    symbol: str = Depends(check_symbol),
    quantity: int,
    user: models.User=Depends(get_current_user_m),
    db: Session = Depends(get_db),
):

    return {"result": "success"}
    
@router.post("/market/short")
async def market_short(
    symbol: str = Depends(check_symbol),
    quantity: int,
    user: models.User=Depends(get_current_user_m),
    db: Session = Depends(get_db),
)
    return {"result": "success"}

@router.post("/market/cover")
async def market_cover(
    symbol: str = Depends(check_symbol),
    quantity: int,
    user: models.User=Depends(get_current_user_m),
    db: Session = Depends(get_db),
)
    return {"result": "success"}

@router.post("/limit/buy")
async def limit_buy(
    symbol: str = Depends(check_symbol),
    quantity: int,
    user: models.User=Depends(get_current_user_m),
    db: Session = Depends(get_db),
)
    return {"result": "success"}

@router.post("/limit/sell")
async def limit_sell(
    symbol: str = Depends(check_symbol),
    quantity: int,
    user: models.User=Depends(get_current_user_m),
    db: Session = Depends(get_db),
)
    return {"result": "success"}

@router.post("/limit/short")
async def limit_short(
    symbol: str = Depends(check_symbol),
    quantity: int,
    user: models.User=Depends(get_current_user_m),
    db: Session = Depends(get_db),
)
    return {"result": "success"}

@router.post("/limit/cover")
async def limit_cover(
    symbol: str = Depends(check_symbol),
    quantity: int,
    user: models.User=Depends(get_current_user_m),
    db: Session = Depends(get_db),
)
    return {"result": "success"}