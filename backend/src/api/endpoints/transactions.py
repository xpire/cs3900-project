from typing import List

from fastapi import Depends
from src import schemas
from src.api.deps import get_current_user_m
from src.models.user import User
from src.schemas.response import ResultAPIRouter
from src.schemas.transaction import TransactionAPIout

router = ResultAPIRouter()


@router.get("/")
async def get_transactions(user_m: User = Depends(get_current_user_m)) -> List[TransactionAPIout]:
    def to_schema(t):
        return schemas.TransactionAPIout(**t.dict(), name=t.stock.name)

    return [to_schema(t) for t in user_m.transaction_hist]
