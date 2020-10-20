from src.models.user import User


def check_exists_watchlist(user: User, symbol: str):

    for entry in user.watchlist:
        if entry.symbol == symbol:
            return True

    return False
