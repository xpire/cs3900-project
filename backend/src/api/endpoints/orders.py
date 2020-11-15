from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
from src import crud
from src import domain_models as dm
from src import schemas
from src.api import common
from src.api.deps import get_current_user_dm, get_db
from src.notification.notifier import send_msg
from src.schemas.response import Result, ResultAPIRouter

router = ResultAPIRouter()


@router.get("")
async def get_orders(user: dm.UserDM = Depends(get_current_user_dm)) -> List[schemas.PendingOrderAPIout]:
    """API endpoint to get list of currently pending orders - both limit orders and aftermarket orders

    Args:
        user (dm.UserDM, optional): user domain model. Defaults to Depends(get_current_user_dm).

    Returns:
        List[schemas.PendingOrderAPIout]: List of pending orders in schema format
    """
    return common.get_orders(user.model)


@router.delete("")
async def delete_order(
    id: int,
    user: dm.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> Result:
    """API endpoint to delete a currently pending order

    Args:
        id (int): ID of the pending order
        user (dm.UserDM, optional): user domain model. Defaults to Depends(get_current_user_dm).
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        Result: Success/Fail
    """
    crud.pending_order.delete_order(db=db, id=id, user=user).ok()
    send_msg(user, "Order successfully cancelled")
    return common.get_orders(user.model)
