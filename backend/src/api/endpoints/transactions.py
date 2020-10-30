from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src import domain_models
from src.api.deps import get_current_user_dm, get_db

router = APIRouter()


@router.get("")
async def get_transactions(
    user: domain_models.UserDM = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
):
    ret = []

    for transaction in user.model.transaction_hist:
        ret += [
            {
                "t_type": transaction.action,
                "symbol": transaction.symbol,
                "name": transaction.stock_info.name,
                "amount": transaction.amount,
                "price": transaction.price,
                "value": transaction.amount * transaction.price,
                "timestamp": transaction.date_time,
            }
        ]

    return ret
