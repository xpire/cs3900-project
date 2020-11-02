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
        ret.append(
            {
                "symbol": transaction.symbol,
                "name": transaction.stock.name,
                "amount": transaction.qty,
                "price": transaction.price,
                "value": transaction.qty * transaction.price,
                "t_type": transaction.trade_type,
                "timestamp": transaction.timestamp,
            }
        )

    return ret
