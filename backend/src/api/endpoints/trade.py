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


def market_order_endpoint(endpoint, trade_type):
    @router.post(endpoint)
    async def market_order(
        quantity: int,
        symbol: str = Depends(check_symbol),
        user: dm.UserDM = Depends(get_current_user_dm),
        db: Session = Depends(get_db),
    ) -> Response:
        return dm.MarketOrder(symbol=symbol, qty=quantity, user=user, db=db, trade_type=trade_type).submit()

    return market_order


def limit_order_endpoint(endpoint, trade_type):
    @router.post(endpoint)
    async def limit_order(
        quantity: int,
        limit: float,  # TODO name changes required
        symbol: str = Depends(check_symbol),
        user: dm.UserDM = Depends(get_current_user_dm),
        db: Session = Depends(get_db),
    ) -> Response:
        return dm.LimitOrder(
            limit_price=limit, symbol=symbol, qty=quantity, user=user, db=db, trade_type=trade_type
        ).submit()

    return limit_order


market_buy = market_order_endpoint("/market/buy", TradeType.BUY)
market_sell = market_order_endpoint("/market/sell", TradeType.SELL)
market_short = market_order_endpoint("/market/short", TradeType.SHORT)
market_cover = market_order_endpoint("/market/cover", TradeType.COVER)

limit_buy = limit_order_endpoint("/limit/buy", TradeType.BUY)
limit_sell = limit_order_endpoint("/limit/sell", TradeType.SELL)
limit_short = limit_order_endpoint("/limit/short", TradeType.SHORT)
limit_cover = limit_order_endpoint("/limit/cover", TradeType.COVER)

"""
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

@router.post("/limit/buy")
async def limit_buy(
    quantity: int,
    limit: float,  # TODO name changes required
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return dm.LimitOrder(limit_price=limit, symbol=symbol, qty=quantity, user=user, db=db, trade_type=TradeType.BUY).submit()


@router.post("/limit/sell")
async def limit_sell(
    quantity: int,
    limit: float,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return dm.LimitOrder(limit_price=limit, symbol=symbol, qty=quantity, user=user, db=db, trade_type=TradeType.SELL).submit()


@router.post("/limit/short")
async def limit_short(
    quantity: int,
    limit: float,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return dm.LimitOrder(limit_price=limit, symbol=symbol, qty=quantity, user=user, db=db, trade_type=TradeType.SHORT).submit()


@router.post("/limit/cover")
async def limit_cover(
    quantity: int,
    limit: float,
    symbol: str = Depends(check_symbol),
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    return dm.LimitOrder(limit_price=limit, symbol=symbol, qty=quantity, user=user, db=db, trade_type=TradeType.COVER).submit()
"""
