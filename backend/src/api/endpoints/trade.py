from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import domain_models as dm
from src.api.deps import check_symbol, get_current_user_dm, get_db
from src.core import trade
from src.crud import crud_user
from src.schemas.response import Response

router = APIRouter()


@router.post("/market/buy")
async def market_buy(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    price = trade.get_stock_price(db, symbol)
    return dm.BuyTrade(symbol=symbol, qty=quantity, price=price, db=db, user=user).execute()


@router.post("/market/sell")
async def market_sell(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
):
    price = trade.get_stock_price(db, symbol)
    return dm.SellTrade(symbol=symbol, qty=quantity, price=price, db=db, user=user).execute()


@router.post("/market/short")
async def market_short(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
):
    price = trade.get_stock_price(db, symbol)
    return dm.ShortTrade(symbol=symbol, qty=quantity, price=price, db=db, user=user).execute()


@router.post("/market/cover")
async def market_cover(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
):
    price = trade.get_stock_price(db, symbol)
    return dm.CoverTrade(symbol=symbol, qty=quantity, price=price, db=db, user=user).execute()


def place_limit_order(
    quantity: int,
    limit: float,
    symbol: str,
    t_type: str,
    user: dm.UserDM,
    db: Session,
) -> Response:
    if quantity < 0:
        raise HTTPException(status_code=400, detail=f"Cannot {t_type} negative quantity")

    if limit < 0:
        raise HTTPException(status_code=400, detail="Limit value cannot be negative")

    crud_user.user.create_order(
        db=db, user_in=user.model, trade_type=t_type, symbol=symbol, quantity=quantity, limit=limit
    )
    # price = trade.get_stock_price(db, symbol)
    # crud_user.user.add_history(
    #     db=db,
    #     user_in=user.model,
    #     price_in=price,
    #     trade_type_in=t_type,
    #     symbol_in=symbol,
    #     amount_in=quantity,
    # )

    return Response(msg="Order placed successfully")


@router.post("/limit/buy")
async def limit_buy(
    quantity: int,
    limit: float,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return place_limit_order(quantity, limit, symbol, "buy", user, db)


@router.post("/limit/sell")
async def limit_sell(
    quantity: int,
    limit: float,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return place_limit_order(quantity, limit, symbol, "sell", user, db)


@router.post("/limit/short")
async def limit_short(
    quantity: int,
    limit: float,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return place_limit_order(quantity, limit, symbol, "short", user, db)


@router.post("/limit/cover")
async def limit_cover(
    quantity: int,
    limit: float,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return place_limit_order(quantity, limit, symbol, "cover", user, db)
