from fastapi import Depends
from sqlalchemy.orm import Session
from src import crud, schemas
from src.api.deps import get_current_user_m, get_db
from src.domain_models import UserDM
from src.domain_models.account_stat_dm import AccountStat
from src.models.user import User
from src.schemas.response import ResultAPIRouter

router = ResultAPIRouter()


@router.get("")
async def get_leaderboard(
    user_m: User = Depends(get_current_user_m), db: Session = Depends(get_db)
) -> schemas.LeaderboardAPIout:
    def to_schema(u):
        net_worth = AccountStat(UserDM(u, db)).net_worth()
        return schemas.LeaderboardUserWithUid(
            uid=u.uid, username=u.username, email=u.email, level=u.level, net_worth=net_worth
        )

    rankings = [to_schema(u) for u in crud.user.get_all_users(db)]
    rankings.sort(key=lambda u: u.net_worth, reverse=True)

    return schemas.LeaderboardAPIout(rankings=rankings[:10], user_ranking=get_rank(rankings, user_m.uid))


def get_rank(rankings, uid):
    for rank, user in enumerate(rankings, 1):
        if user.uid == uid:
            return rank
