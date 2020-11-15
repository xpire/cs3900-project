from typing import List

from fastapi import Depends
from src import schemas
from src.api import common
from src.api.deps import get_current_user_m
from src.models.user import User
from src.schemas.response import ResultAPIRouter
from src.schemas.transaction import TransactionAPIout

router = ResultAPIRouter()


@router.get("/")
async def get_transactions(user_m: User = Depends(get_current_user_m)) -> List[TransactionAPIout]:
    """API endpoint to get a users transaction history

    Args:
        user_m (User, optional): user model. Defaults to Depends(get_current_user_m).

    Returns:
        List[TransactionAPIout]: List of executed and cancelled transactions the user has made
    """
    return common.get_transactions(user_m)
