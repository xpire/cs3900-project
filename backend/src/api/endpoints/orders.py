from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src import crud
from src import domain_models as dm
from src import schemas
from src.api.deps import get_current_user_dm, get_db
from src.core.utilities import HTTP400
from src.schemas.response import Response, Success

router = APIRouter()


@router.get("")
async def get_orders(user: dm.UserDM = Depends(get_current_user_dm), db: Session = Depends(get_db)):
    print(user.model.pending_orders)
    print(user.model.limit_orders)
    print(user.model.after_orders)

    def to_response(order):
        return schemas.PendingOrderAPIout(**order.__dict__, exchange=order.stock.exchange)

    return [to_response(x) for x in user.model.pending_orders]


@router.delete("")
async def delete_order(
    id: int,
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:

    crud.pending_order.delete_order(db=db, id=id, user=user).assert_ok()
    return Success("Order successfully cancelled")
