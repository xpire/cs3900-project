from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
from src import crud
from src import models
from src.api.deps import check_symbol, get_current_user_m, get_db
from src.schemas.response import Result, ResultAPIRouter, Success
from src.schemas.stock import StockAPIout

router = ResultAPIRouter()


@router.get("")
async def get_watchlist(
    user_m: models.User = Depends(get_current_user_m), db: Session = Depends(get_db)
) -> List[StockAPIout]:
    """API endpoint to get a users watchlist

    Args:
        user_m (models.User, optional): user model. Defaults to Depends(get_current_user_m).
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        List[StockAPIout]: List of stocks (and their information) in the users watchlist
    """
    return [x.stock for x in user_m.watchlist]


@router.post("")
async def update_watchlist(
    symbol: str = Depends(check_symbol),
    user_m: models.user = Depends(get_current_user_m),
    db: Session = Depends(get_db),
) -> Result:
    """API endpoint to add a stock to the users watchlist

    Args:
        symbol (str, optional): stock symbol. Defaults to Depends(check_symbol).
        user_m (models.user, optional): user model. Defaults to Depends(get_current_user_m).
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        Result: Fail/Success
    """
    crud.user.add_to_watchlist(symbol=symbol, db=db, user=user_m).ok()
    return Success(f"{symbol} added to watchlist")


@router.delete("")
async def delete_watchlist(
    symbol: str = Depends(check_symbol),
    user_m: models.user = Depends(get_current_user_m),
    db: Session = Depends(get_db),
) -> Result:
    """API endpoint to delete a stock from the users watchlist

    Args:
        symbol (str, optional): stock symbol. Defaults to Depends(check_symbol).
        user_m (models.user, optional): user model. Defaults to Depends(get_current_user_m).
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        Result: Success/Fail
    """
    crud.user.delete_from_watchlist(symbol=symbol, db=db, user=user_m).ok()
    return Success(f"{symbol} removed from watchlist")
