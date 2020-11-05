from typing import List

from fastapi import Depends
from src import domain_models as dm
from src import schemas
from src.api.deps import get_current_user_dm
from src.schemas.response import ResultAPIRouter

router = ResultAPIRouter()


@router.get("")
async def get_portfolio(user: dm.UserDM = Depends(get_current_user_dm),) -> schemas.PortfolioAPIout:
    stat = dm.AccountStat(user)
    return schemas.PortfolioAPIout(
        long=stat.get_positions_info(is_long=True), short=stat.get_positions_info(is_long=False)
    )


@router.get("/stats")
async def get_portfolio_stats(user: dm.UserDM = Depends(get_current_user_dm),) -> schemas.PortfolioStatAPIout:
    return dm.AccountStat(user).compile_portfolio_stats()


@router.get("/history")
async def get_net_worth_history(
    user: dm.UserDM = Depends(get_current_user_dm),
) -> List[schemas.NetWorthTimeSeriesAPIout]:
    return dm.AccountStat(user).get_net_worth_history()
