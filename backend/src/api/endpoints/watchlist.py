from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src import crud
from src import domain_models as dm
from src import models
from src.api.deps import check_symbol, get_current_user_m, get_db
from src.schemas.response import Response, Success, return_response
from src.schemas.stock import StockAPIout

router = APIRouter()


@router.get("")
async def get_watchlist(
    user_m: models.User = Depends(get_current_user_m), db: Session = Depends(get_db)
) -> List[StockAPIout]:
    return [x.stock for x in user_m.watchlist]


@router.post("")
@return_response()
async def update_watchlist(
    symbol: str = Depends(check_symbol),
    user_m: models.user = Depends(get_current_user_m),
    db: Session = Depends(get_db),
) -> Response:
    crud.user.add_to_watchlist(symbol=symbol, db=db, user=user_m).assert_ok()
    return Success(f"{symbol} added to watchlist")


@router.delete("")
@return_response()
async def delete_watchlist(
    symbol: str = Depends(check_symbol),
    user_m: models.user = Depends(get_current_user_m),
    db: Session = Depends(get_db),
) -> Response:
    crud.user.delete_from_watchlist(symbol=symbol, db=db, user=user_m).assert_ok()
    return Success(f"{symbol} removed from watchlist")
