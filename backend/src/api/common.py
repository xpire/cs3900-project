from typing import List

from firebase_admin import auth
from src import crud
from src import domain_models as dm
from src import schemas
from src.core.utilities import log_msg
from src.domain_models.trading_hours import trading_hours_manager
from src.domain_models.user_dm import UserDM


def get_user_detail(user) -> schemas.UserDetailAPIout:
    user_m = user.model
    return schemas.UserDetailAPIout(
        basic=get_basic_detail(user),
        watchlist=get_watchlist(user_m),
        orders=get_orders(user_m),
        transactions=get_transactions(user_m),
        portfolio=get_portfolio(user),
        stats=get_portfolio_stats(user),
        leaderboard=get_leaderboard(user),
        notifications=get_notifications(user_m),
    )


def get_basic_detail(user) -> schemas.BasicDetail:
    return schemas.BasicDetail(**user.schema.dict())


def get_watchlist(user_m) -> List[schemas.StockAPIout]:
    def to_schema(stock):
        return schemas.StockAPIout(**stock.dict())

    return [to_schema(x.stock) for x in user_m.watchlist]


def stock_to_realtime_schema(stock) -> schemas.StockRealTimeAPIout:
    return schemas.StockRealTimeAPIout(
        **stock.dict(),
        **dm.get_data_provider().data[stock.symbol],
        **trading_hours_manager.get_trading_hours_info(stock).dict(),
    )


def get_orders(user_m) -> List[schemas.PendingOrderAPIout]:
    def to_schema(order):
        return schemas.PendingOrderAPIout(**order.dict(), exchange=order.stock.exchange, name=order.stock.name)

    return [to_schema(x) for x in user_m.pending_orders]


def get_transactions(user_m) -> List[schemas.TransactionAPIout]:
    def to_schema(t):
        return schemas.TransactionAPIout(**t.dict(), name=t.stock.name)

    return [to_schema(t) for t in user_m.transaction_hist]


def get_portfolio(user) -> schemas.PortfolioAPIout:
    stat = dm.AccountStat(user)
    return schemas.PortfolioAPIout(
        long=stat.get_positions_info(is_long=True), short=stat.get_positions_info(is_long=False)
    )


def get_portfolio_stats(user) -> schemas.PortfolioStatAPIout:
    return dm.AccountStat(user).compile_portfolio_stats()


def get_leaderboard(user) -> schemas.LeaderboardAPIout:
    db = user.db

    def to_schema(u):
        net_worth = dm.AccountStat(UserDM(u, db)).net_worth()
        return schemas.LeaderboardUserWithUid(
            uid=u.uid, username=u.username, email=u.email, level=u.level, net_worth=net_worth
        )

    rankings = [to_schema(u) for u in crud.user.get_all_users(db) if (auth.get_user(u.uid).email_verified)] 
    rankings.sort(key=lambda u: u.net_worth, reverse=True)

    return schemas.LeaderboardAPIout(rankings=rankings[:10], user_ranking=get_rank(rankings, user.model.uid))


def get_rank(rankings, uid):
    """Gets a user's current leaderboard ranking

    Args:
        rankings (List[schemas.LeaderboardUserWithUid]): user information for leaderboard
        uid (str): user id

    Returns:
        int: users ranking
    """
    for rank, user in enumerate(rankings, 1):
        if user.uid == uid:
            return rank


def get_notifications(user_m) -> schemas.NotificationAPIout:
    def to_schema(notif):
        return schemas.NotificationAPIout(**notif.dict())

    return [to_schema(x) for x in user_m.notifications]
