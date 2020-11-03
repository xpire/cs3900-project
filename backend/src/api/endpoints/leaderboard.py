from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src import crud, schemas
from src.api.deps import get_current_user_m, get_db
from src.domain_models import UserDM
from src.models.user import User
from src.schemas.user import LeaderboardAPIout

router = APIRouter()


@router.get("")
async def get_leaderboard(
    user_m: User = Depends(get_current_user_m), db: Session = Depends(get_db)
) -> schemas.LeaderboardAPIout:
    def to_user_info(u):
        net_worth = UserDM(u, db).get_net_value()
        return schemas.UserLeaderboardAPIout(username=u.username, email=u.email, level=u.level, net_worth=net_worth)

    rankings = [to_user_info(u) for u in crud.user.get_all_users(db)]
    rankings.sort(key=lambda e: e.net_worth, reverse=True)

    return LeaderboardAPIout(rankings=rankings[:10], user_ranking=get_rank(rankings, user_m.uid))


def get_rank(rankings, uid):
    for rank, user in enumerate(rankings, 1):
        if user.uid == uid:
            return rank
