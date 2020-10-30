import src.api.endpoints.stocks as stocks_api
from src.domain_models.user_dm import UserDM


def get_stock_price(symbol: str):
    return stocks_api.market_data_provider.get_curr_day_close(symbol)


def apply_commission(price: float, is_buying: bool = True):
    return price * 1.005 if is_buying else price * 0.995


def check_owned(user: UserDM, qty: int, symbol: str, positions):
    pos = next((x for x in positions if x.symbol == symbol), None)
    if pos is None:
        return False

    return pos is not None and qty <= pos.amount


def check_owned_longs(user: UserDM, qty: int, symbol: str):
    return check_owned(user, qty, symbol, user.model.long_positions)


def check_owned_shorts(user: UserDM, qty: int, symbol: str):
    return check_owned(user, qty, symbol, user.model.short_positions)


def check_short_balance(user: UserDM, total_price: float):
    return total_price <= user.get_short_balance()
