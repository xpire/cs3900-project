from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import crud
from src.api.deps import check_symbol, get_current_user_dm, get_db
from src.core.config import settings
from src.core.utilities import fail_save, log_msg
from src.crud.crud_stock import stock
from src.db.session import SessionLocal
from src.domain_models import UserDM

router = APIRouter()


@router.get("")
async def get_leaderboard(user: UserDM = Depends(get_current_user_dm), db: Session = Depends(get_db)):

    ret = {}

    rankings = []  # Entries are (uid, net_worth)
    users = crud.user.get_all_users(db)
    for u in users:
        user_dm = get_current_user_dm(crud.user.get_user_by_uid(db=db, uid=u.uid), db)
        net_worth = user_dm.get_net_value()
        rankings += [
            {
                "uid": user_dm.model.uid,
                "username": user_dm.model.username,
                "email": user_dm.model.email,
                "net_worth": net_worth,
                "level": user_dm.model.level,
            }
        ]

    # Sort by the net worth in descending order
    rankings.sort(key=lambda e: -e["net_worth"])

    ret["user_ranking"] = get_rank(rankings, user.model.uid)
    ret["rankings"] = rankings[:10]  # Return top 10 users
    return ret


def get_rank(rankings, uid):
    for i, entry in enumerate(rankings):
        if entry["uid"] == uid:
            return i + 1
