from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import domain_models, schemas
from src.api.deps import check_symbol, get_current_user_dm, get_db
from src.core import trade
from src.core.config import settings
from src.crud import crud_stock, crud_user
from src.db.session import SessionLocal
from src.schemas.response import Response

router = APIRouter()


@router.get("")
async def get_orders(user: domain_models.UserDM = Depends(get_current_user_dm), db: Session = Depends(get_db)):
    ret = []
    for order in user.model.limit_orders:
        ret.append(
            {
                "id": order.id,
                "name": order.stock_info.name,
                "symbol": order.symbol,
                "type": order.t_type,
                "quantity": order.amount,
                "price": order.price,
                "exchange": order.stock_info.exchange,
                "is_limit": True,
            }
        )

    """
    for order in user.model.after_orders:
        ret.append(
            {
                "id": order.id,
                "name": order.stock_info.name,
                "symbol": order.symbol,
                "type": order.t_type,
                "quantity": order.amount,
                "price": order.price,
                "exchange": order.stock_info.exchange,
                "is_limit": False,
            }
        )
    """

    return ret


@router.delete("")
async def delete_order(
    identity: int,
    is_limit: bool,
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    if not user.check_order_exists(id=identity, is_limit=is_limit):
        raise HTTPException(status_code=400, detail=f"Order {identity} does not exist")

    if is_limit:
        crud_user.user.delete_order(db=db, user_in=user.model, identity=identity)
    else:
        pass
        # TODO: update with db
        # crud_user.user.delete_after_order(db=db, user_in=user.model, identity=identity)

    return Response(msg="Order removed")
