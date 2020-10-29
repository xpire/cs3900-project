from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src import domain_models, models
from src.api.deps import check_symbol, get_current_user_dm, get_current_user_m, get_db
from src.schemas.response import Response
from src.core.utilities import HTTP400

router = APIRouter()


@router.get("")
async def get_watchlist(user: models.User = Depends(get_current_user_m), db: Session = Depends(get_db)):
    ret = []
    for entry in user.watchlist:
        ret += [
            {
                "name": entry.stock_info.name,
                "symbol": entry.stock_info.symbol,
                "exchange": entry.stock_info.exchange,
            }
        ]

    return ret


@router.post("")
async def update_watchlist(
    symbol: str = Depends(check_symbol),
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:

    if user.check_exists_watchlist(symbol):
        raise HTTP400(f"Symbol {symbol} already exists in watchlist.")

    user.watchlist_create(symbol)

    return Response(msg=f"{symbol} added to watchlist")


@router.delete("")
async def delete_watchlist(
    symbol: str = Depends(check_symbol),
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:

    if not user.check_exists_watchlist(symbol):
        raise HTTP400(f"Symbol {symbol} does not exist in watchlist.")

    user.watchlist_delete(symbol)

    return Response(msg=f"{symbol} removed from watchlist")
