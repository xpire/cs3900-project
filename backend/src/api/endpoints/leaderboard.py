from fastapi import Depends
from sqlalchemy.orm import Session
from src import crud
from src import domain_models as dm
from src import schemas
from src.api import common
from src.api.deps import get_current_user_dm, get_db
from src.schemas.response import ResultAPIRouter

router = ResultAPIRouter()


@router.get("")
async def get_leaderboard(
    user: dm.UserDM = Depends(get_current_user_dm), db: Session = Depends(get_db)
) -> schemas.LeaderboardAPIout:
    """API endpoint to get current leaderboard

    Args:
        user (dm.UserDM, optional): user domain model. Defaults to Depends(get_current_user_dm).
        db (Session, optional): databse session. Defaults to Depends(get_db).

    Returns:
        schemas.LeaderboardAPIout: Leaderboard information as per LeaderboardAPIout schema
    """
    return common.get_leaderboard(user)
