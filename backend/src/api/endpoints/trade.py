from fastapi import Depends
from sqlalchemy.orm import Session
from src import domain_models as dm
from src.api.deps import check_symbol, get_current_user_dm, get_db
from src.schemas.response import Result, ResultAPIRouter
from src.schemas.transaction import TradeType

router = ResultAPIRouter()


def market_order_endpoint(endpoint, trade_type):
    """Wrapper function for API market orders

    Args:
        endpoint (str): market endpoint to hit
        trade_type (TradeType): type of market trade to make

    Returns:
        MarketOrder: market order endpoint return
    """

    @router.post(endpoint)
    async def market_order(
        quantity: int,
        symbol: str = Depends(check_symbol),
        user: dm.UserDM = Depends(get_current_user_dm),
        db: Session = Depends(get_db),
    ) -> Result:
        """API endpoint to make a market order

        Args:
            quantity (int): amount of the stock to trade
            symbol (str, optional): stock symbol. Defaults to Depends(check_symbol).
            user (dm.UserDM, optional): user domain model. Defaults to Depends(get_current_user_dm).
            db (Session, optional): database session. Defaults to Depends(get_db).

        Returns:
            Result: Success/Fail
        """
        return dm.MarketOrder(symbol=symbol, qty=quantity, user=user, db=db, trade_type=trade_type).submit()

    return market_order


def limit_order_endpoint(endpoint, trade_type):
    """Wrapper function for API limit orders

    Args:
        endpoint (str): limit API to hit
        trade_type (TradeType): type of limit order to palce

    Returns:
        LimitOrder: limit_order endpoint return
    """

    @router.post(endpoint)
    async def limit_order(
        quantity: int,
        limit: float,
        symbol: str = Depends(check_symbol),
        user: dm.UserDM = Depends(get_current_user_dm),
        db: Session = Depends(get_db),
    ) -> Result:
        """API endpoint to make limit orders

        Args:
            quantity (int): amount of the stock to trade
            limit (float): limit price for the order to be executed at
            symbol (str, optional): stock symbol. Defaults to Depends(check_symbol).
            user (dm.UserDM, optional): user domain model. Defaults to Depends(get_current_user_dm).
            db (Session, optional): database session. Defaults to Depends(get_db).

        Returns:
            Result: Success/Fail
        """
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
