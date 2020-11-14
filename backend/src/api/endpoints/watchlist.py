from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
from src import crud, models
from src.api import common
from src.api.deps import check_symbol, get_current_user_dm, get_current_user_m, get_db
from src.domain_models.user_dm import UserDM
from src.notification.notifier import send_msg
from src.schemas.response import ResultAPIRouter
from src.schemas.stock import StockAPIout

router = ResultAPIRouter()


@router.get("")
async def get_watchlist(user_m: models.User = Depends(get_current_user_m)) -> List[StockAPIout]:
    """API endpoint to get a users watchlist

    Args:
        user_m (models.User, optional): user model. Defaults to Depends(get_current_user_m).

    Returns:
        List[StockAPIout]: List of stocks (and their information) in the users watchlist
    """
    return common.get_watchlist(user_m)


@router.post("")
async def update_watchlist(
    symbol: str = Depends(check_symbol),
    user: UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> List[StockAPIout]:
    """API endpoint to add a stock to the users watchlist

    Args:
        symbol (str, optional): stock symbol. Defaults to Depends(check_symbol).
        user (UserDM, optional): user domain model. Defaults to Depends(get_current_user_dm).
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        List[StockAPIout]: List of stocks (and their information) in the users watchlist
    """
    crud.user.add_to_watchlist(symbol=symbol, db=db, user=user.model).ok()
    send_msg(user, f"{symbol} added to watchlist")
    return common.get_watchlist(user.model)


@router.delete("")
async def delete_watchlist(
    symbol: str = Depends(check_symbol),
    user: UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> List[StockAPIout]:
    """API endpoint to delete a stock from the users watchlist

    Args:
        symbol (str, optional): stock symbol. Defaults to Depends(check_symbol).
        user (UserDM, optional): user domain model. Defaults to Depends(get_current_user_dm).
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        List[StockAPIout]: List of stocks (and their information) in the users watchlist
    """
    crud.user.delete_from_watchlist(symbol=symbol, db=db, user=user.model).ok()
    send_msg(user, f"{symbol} removed from watchlist")
    return common.get_watchlist(user.model)
