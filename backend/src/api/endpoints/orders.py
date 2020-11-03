from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src import crud
from src import domain_models as dm
from src import schemas
from src.api.deps import get_current_user_dm, get_db
from src.schemas.response import Response, Success, return_response

router = APIRouter()


@router.get("")
async def get_orders(user: dm.UserDM = Depends(get_current_user_dm)) -> List[schemas.PendingOrderAPIout]:
    def to_response(order):
        print(order.dict())
        return schemas.PendingOrderAPIout(**order.dict(), exchange=order.stock.exchange)

    return [to_response(x) for x in user.model.pending_orders]


@router.delete("")
@return_response()
async def delete_order(
    id: int,
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    crud.pending_order.delete_order(db=db, id=id, user=user).assert_ok()
    return Success("Order successfully cancelled")
