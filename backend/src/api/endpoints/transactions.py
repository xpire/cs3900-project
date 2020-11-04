from typing import List

from fastapi import APIRouter, Depends
from src import schemas
from src.api.deps import get_current_user_m
from src.models.user import User
from src.schemas.transaction import TransactionAPIout

router = APIRouter()


@router.get("/")
async def get_transactions(user_m: User = Depends(get_current_user_m)) -> List[TransactionAPIout]:
    def to_transaction(t):
        return schemas.TransactionAPIout(**t.dict(), name=t.stock.name)

    return [to_transaction(t) for t in user_m.transaction_hist]
