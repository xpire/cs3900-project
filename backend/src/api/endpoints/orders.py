from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src import domain_models
from src.api.deps import get_current_user_dm, get_db
from src.crud import crud_user
from src.schemas.response import Response
from src.core.utilities import HTTP400

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

    for order in user.model.after_orders:
        ret.append(
            {
                "id": order.id,
                "name": order.stock_info.name,
                "symbol": order.symbol,
                "type": order.t_type,
                "quantity": order.amount,
                "exchange": order.stock_info.exchange,
                "is_limit": False,
            }
        )

    return ret


@router.delete("")
async def delete_order(
    identity: int,
    is_limit: bool,
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Response:
    if not user.check_order_exists(id=identity, is_limit=is_limit):
        raise HTTP400(f"Order {identity} does not exist")

    if is_limit:
        crud_user.user.delete_order(db=db, user_in=user.model, identity=identity)
    else:
        pass
        crud_user.user.delete_after_order(db=db, user_in=user.model, identity=identity)

    return Response(msg="Order removed")
