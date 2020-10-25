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
async def get_orders(
    user: domain_models.UserDM=Depends(get_current_user_dm),
    db: Session = Depends(get_db)
):
    ret = []
    for order in user.model.limit_orders:
        ret.append(
            {
                "id" : order.id,
                "name" : order.stock_info.name,
                "symbol" : order.symbol,
                "type" : order.t_type,
                "quantity" : order.amount,
                "price" : order.price,
                "exchange" : order.stock_info.exchange
            }
        )

    return ret

@router.delete("")
async def delete_order(
    identity: int,
    user: domain_models.UserDM=Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    if not user.check_order_exists(identity):
        raise HTTPException(status_code=400, detail=f"Order {identity} does not exist")

    crud_user.user.delete_order(db=db, user_in=user.model, identity=identity)

    return Response("Order removed")
