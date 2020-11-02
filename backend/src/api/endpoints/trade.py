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

# TODO change endpoint parameter names
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
        limit: float,
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
