from typing import List

from fastapi import Depends
from src import domain_models as dm
from src import schemas
from src.api import common
from src.api.deps import get_current_user_dm
from src.schemas.response import ResultAPIRouter

router = ResultAPIRouter()


@router.get("")
async def get_portfolio(
    user: dm.UserDM = Depends(get_current_user_dm),
) -> schemas.PortfolioAPIout:
    """API endpoint to get a users current portfolio positions - both long and shorts

    Args:
        user (dm.UserDM, optional): user domain model. Defaults to Depends(get_current_user_dm).

    Returns:
        schemas.PortfolioAPIout: List of portfolio positions
    """
    return common.get_portfolio(user)


@router.get("/stats")
async def get_portfolio_stats(
    user: dm.UserDM = Depends(get_current_user_dm),
) -> schemas.PortfolioStatAPIout:
    """API endpoint to get a users portfolios statistics

    Args:
        user (dm.UserDM, optional): user domain model. Defaults to Depends(get_current_user_dm).

    Returns:
        schemas.PortfolioStatAPIout: complete portfolio statistics
    """
    return common.get_portfolio_stats(user)


@router.get("/history")
async def get_net_worth_history(
    user: dm.UserDM = Depends(get_current_user_dm),
) -> List[schemas.NetWorthTimeSeriesBase]:
    """API endpoint to get the history of a users net worth (for graphing purposes)

    Args:
        user (dm.UserDM, optional): user domain model. Defaults to Depends(get_current_user_dm).

    Returns:
        List[schemas.NetWorthTimeSeriesBase]: List of users net worth values, snapshotted at regular intervals
    """
    return dm.AccountStat(user).get_net_worth_history()
