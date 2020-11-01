from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src import domain_models as dm
from src.api.deps import check_symbol, get_current_user_dm, get_db
from src.core import trade
from src.core.utilities import HTTP400
from src.crud import crud_user, stock
from src.domain_models.trade_dm import Trade
from src.domain_models.trading_hours import trading_hours_manager
from src.schemas.response import Response
from src.schemas.transaction import TradeType

router = APIRouter()


@router.post("/market/buy")
async def market_buy(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    price = trade.get_stock_price(symbol)

    if trading_hours_manager.is_trading(stock=stock.get_stock_by_symbol(db=db, stock_symbol=symbol)):
        # return dm.BuyTrade(symbol=symbol, qty=quantity, price=price, db=db, user=user).execute()
        return dm.Trade.new(TradeType.BUY, symbol=symbol, qty=quantity, price=price, db=db, user=user).execute()
    else:
        crud_user.user.add_after_order(
            db=db,
            user_in=user.model,
            trade_type_in=TradeType.BUY,
            amount_in=quantity,
            symbol_in=symbol,
            dt_in=datetime.now(),
        )
        return Response(msg="After market order placed")


@router.post("/market/sell")
async def market_sell(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
):
    price = trade.get_stock_price(symbol)

    if trading_hours_manager.is_trading(stock=stock.get_stock_by_symbol(db=db, stock_symbol=symbol)):
        return dm.SellTrade(symbol=symbol, qty=quantity, price=price, db=db, user=user).execute()
    else:
        crud_user.user.add_after_order(
            db=db,
            user_in=user.model,
            trade_type_in=TradeType.SELL,
            amount_in=quantity,
            symbol_in=symbol,
            dt_in=datetime.now(),
        )
        return Response(msg="After market order placed")


@router.post("/market/short")
async def market_short(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
):
    price = trade.get_stock_price(symbol)

    if trading_hours_manager.is_trading(stock=stock.get_stock_by_symbol(db=db, stock_symbol=symbol)):
        return dm.ShortTrade(symbol=symbol, qty=quantity, price=price, db=db, user=user).execute()
    else:
        crud_user.user.add_after_order(
            db=db,
            user_in=user.model,
            trade_type_in=TradeType.SHORT,
            amount_in=quantity,
            symbol_in=symbol,
            dt_in=datetime.now(),
        )
        return Response(msg="After market order placed")


@router.post("/market/cover")
async def market_cover(
    quantity: int,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
):
    price = trade.get_stock_price(symbol)

    if trading_hours_manager.is_trading(stock=stock.get_stock_by_symbol(db=db, stock_symbol=symbol)):
        return dm.CoverTrade(symbol=symbol, qty=quantity, price=price, db=db, user=user).execute()
    else:
        crud_user.user.add_after_order(
            db=db,
            user_in=user.model,
            trade_type_in=TradeType.COVER,
            amount_in=quantity,
            symbol_in=symbol,
            dt_in=datetime.now(),
        )
        return Response(msg="After market order placed")


# TODO change quantity to qty
def place_limit_order(
    quantity: int,
    limit: float,
    symbol: str,
    t_type: TradeType,
    user: dm.UserDM,
    db: Session,
) -> Response:
    if quantity < 0:
        raise HTTP400(f"Cannot {t_type} negative quantity")

    if limit < 0:
        raise HTTP400("Limit value cannot be negative")

    crud_user.user.create_order(
        db=db, user_in=user.model, trade_type=t_type, symbol=symbol, quantity=quantity, limit=limit
    )

    return Response(msg="Order placed successfully")


@router.post("/limit/buy")
async def limit_buy(
    quantity: int,
    limit: float,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return place_limit_order(quantity, limit, symbol, TradeType.BUY, user, db)


@router.post("/limit/sell")
async def limit_sell(
    quantity: int,
    limit: float,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return place_limit_order(quantity, limit, symbol, TradeType.SELL, user, db)


@router.post("/limit/short")
async def limit_short(
    quantity: int,
    limit: float,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return place_limit_order(quantity, limit, symbol, TradeType.SHORT, user, db)


@router.post("/limit/cover")
async def limit_cover(
    quantity: int,
    limit: float,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return place_limit_order(quantity, limit, symbol, TradeType.COVER, user, db)
