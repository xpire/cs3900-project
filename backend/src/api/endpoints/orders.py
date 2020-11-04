from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
from src import crud
from src import domain_models as dm
from src import schemas
from src.api.deps import get_current_user_dm, get_db
from src.schemas.response import Result, ResultAPIRouter, Success

router = ResultAPIRouter()


@router.get("")
async def get_orders(user: dm.UserDM = Depends(get_current_user_dm)) -> List[schemas.PendingOrderAPIout]:
    def to_schema(order):
        return schemas.PendingOrderAPIout(**order.dict(), exchange=order.stock.exchange)

    return [to_schema(x) for x in user.model.pending_orders]


@router.delete("")
async def delete_order(
    id: int,
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Result:
    crud.pending_order.delete_order(db=db, id=id, user=user).ok()
    return Success("Order successfully cancelled")
