from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import domain_models, schemas
from src.crud import crud_user, crud_stock
from src.core import trade
from src.api.deps import check_symbol, get_current_user_dm, get_db
from src.core.config import settings
from src.db.session import SessionLocal
from src.schemas.response import Response

router = APIRouter()

# TODO: enforce trading hours


@router.post("/market/buy")
async def market_buy(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    if quantity < 0:
        raise HTTPException(status_code=400, detail="Cannot buy negative quantity")

    curr_stock_price = trade.get_stock_price(db, symbol)
    trade_price = trade.apply_commission(curr_stock_price * quantity)

    if user.model.balance < trade_price:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    crud_user.user.add_transaction(
        db, user.model, "long", symbol, quantity, curr_stock_price
    )

    new_balance = user.model.balance - trade_price
    crud_user.user.update_balance(db, user.model, new_balance)

    return Response("Trade successful")


@router.post("/market/sell")
async def market_sell(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:

    if quantity < 0:
        raise HTTPException(status_code=400, detail="Cannot sell negative quantity")

    if not trade.check_owned_longs(user, quantity, symbol):
        raise HTTPException(status_code=400, detail="Cannot sell more than owned")

    curr_stock_price = trade.get_stock_price(db, symbol)
    trade_price = trade.apply_commission(curr_stock_price * quantity, False)

    crud_user.user.deduct_transaction(db, user.model, "long", symbol, quantity)

    new_balance = user.model.balance + trade_price
    crud_user.user.update_balance(db, user.model, new_balance)

    return Response("Trade successful")


@router.post("/market/short")
async def market_short(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    if quantity < 0:
        raise HTTPException(status_code=400, detail="Cannot short negative quantity")

    curr_stock_price = trade.get_stock_price(db, symbol)
    trade_price = curr_stock_price * quantity

    if not trade.check_short_balance(user, trade_price):
        raise HTTPException(status_code=400, detail="Insufficient short balance")

    final_trade_price = trade.apply_commission(trade_price, False)

    crud_user.user.add_transaction(
        db, user.model, "short", symbol, quantity, curr_stock_price
    )

    new_balance = user.model.balance + final_trade_price
    crud_user.user.update_balance(db, user.model, new_balance)

    return Response("Trade successful")


@router.post("/market/cover")
async def market_cover(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Reponse:
    if quantity < 0:
        raise HTTPException(status_code=400, detail="Cannot cover negative quantity")

    curr_stock_price = trade.get_stock_price(db, symbol)
    trade_price = trade.apply_commission(curr_stock_price * quantity)

    if not trade.check_owned_shorts(user, quantity, symbol):
        raise HTTPException(status_code=400, detail="Cannot cover more than owed")

    if user.model.balance < trade_price:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    crud_user.user.deduct_transaction(db, user.model, "short", symbol, quantity)

    new_balance = user.model.balance - trade_price
    crud_user.user.update_balance(db, user.model, new_balance)

    return Response("Trade successful")


async def place_limit_order(
    quantity: int,
    limit: float,
    symbol: str,
    t_type: str,
    user: domain_models.UserDM,
    db: Session,
) -> Response:
    if quantity < 0:
        raise HTTPException(
            status_code=400, detail=f"Cannot {t_type} negative quantity"
        )

    if limit < 0:
        raise HTTPException(status_code=400, detail="Limit value cannot be negative")

    crud_user.user.create_order(db, user.model, t_type, symbol, quantity, limit)

    return Response("Order placed successfully")


@router.post("/limit/buy")
async def limit_buy(
    quantity: int,
    limit: float,
    symbol: str = Depends(check_symbol),
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return place_limit_order(db, user, "buy", symbol, quantity, limit)


@router.post("/limit/sell")
async def limit_sell(
    quantity: int,
    limit: float,
    symbol: str = Depends(check_symbol),
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return place_limit_order(db, user, "sell", symbol, quantity, limit)


@router.post("/limit/short")
async def limit_short(
    quantity: int,
    limit: float,
    symbol: str = Depends(check_symbol),
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return place_limit_order(db, user, "short", symbol, quantity, limit)


@router.post("/limit/cover")
async def limit_cover(
    quantity: int,
    limit: float,
    symbol: str = Depends(check_symbol),
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return place_limit_order(db, user, "cover", symbol, quantity, limit)