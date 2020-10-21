from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import models, schemas
from src.crud import crud_user, crud_stock
from src.core import trade
from src.api.deps import check_symbol, decode_token, get_current_user_m, get_db
from src.core.config import settings
from src.db.session import SessionLocal

router = APIRouter()


@router.post("/market/buy")
async def market_buy(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: models.User = Depends(get_current_user_m),
    db: Session = Depends(get_db),
):
    if quantity < 0:
        return {"result": "cannot buy negative quantity"}

    curr_stock_price = trade.get_stock_price(db, symbol)
    trade_price = trade.get_trade_price(curr_stock_price, quantity)

    if not trade.check_balance(user, trade_price):
        return {"result": "insufficient balance"}

    crud_user.user.add_to_portfolio(db, user, symbol, quantity, curr_stock_price)

    new_balance = user.balance - trade_price
    crud_user.user.update_balance(db, user, new_balance)

    return {"result": "success"}


@router.post("/market/sell")
async def market_sell(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: models.User = Depends(get_current_user_m),
    db: Session = Depends(get_db),
):

    if quantity < 0:
        return {"result": "cannot sell negative quantity"}

    if not trade.check_owned_stocks(user, quantity, symbol):
        return {"result": "cannot sell more than owned"}

    curr_stock_price = trade.get_stock_price(db, symbol)
    trade_price = trade.get_trade_price(curr_stock_price, quantity, False)

    crud_user.user.deduct_from_portfolio(db, user, symbol, quantity)

    new_balance = user.balance + trade_price
    crud_user.user.update_balance(db, user, new_balance)

    return {"result": "success"}


@router.post("/market/short")
async def market_short(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: models.User = Depends(get_current_user_m),
    db: Session = Depends(get_db),
):
    return {"result": "success"}


@router.post("/market/cover")
async def market_cover(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: models.User = Depends(get_current_user_m),
    db: Session = Depends(get_db),
):
    return {"result": "success"}


@router.post("/limit/buy")
async def limit_buy(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: models.User = Depends(get_current_user_m),
    db: Session = Depends(get_db),
):
    return {"result": "success"}


@router.post("/limit/sell")
async def limit_sell(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: models.User = Depends(get_current_user_m),
    db: Session = Depends(get_db),
):
    return {"result": "success"}


@router.post("/limit/short")
async def limit_short(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: models.User = Depends(get_current_user_m),
    db: Session = Depends(get_db),
):
    return {"result": "success"}


@router.post("/limit/cover")
async def limit_cover(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: models.User = Depends(get_current_user_m),
    db: Session = Depends(get_db),
):
    return {"result": "success"}