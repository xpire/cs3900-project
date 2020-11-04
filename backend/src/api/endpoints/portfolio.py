from fastapi import APIRouter, Depends
from src import domain_models as dm
from src import schemas
from src.api.deps import get_current_user_dm

router = APIRouter()


@router.get("")
async def get_portfolio(
    user: dm.UserDM = Depends(get_current_user_dm),
) -> schemas.PortfolioAPIout:
    stat = dm.AccountStat(user)
    return schemas.PortfolioAPIout(
        long=stat.get_positions_info(is_long=True), short=stat.get_positions_info(is_long=False)
    )


@router.get("/stats")
async def get_portfolio_stats(
    user: dm.UserDM = Depends(get_current_user_dm),
) -> schemas.PortfolioStatAPIout:
    return dm.AccountStat(user).compile_portfolio_stats()
