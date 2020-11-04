from src.core.config import settings
from src.core.utilities import find
from src.domain_models.account_stat_dm import AccountStat
from src.domain_models.user_dm import UserDM


def apply_commission(price: float, is_buying: bool = True):
    rate = 1 + (1 if is_buying else -1) * settings.COMMISSION_RATE
    return price * rate


def check_owned(qty: int, symbol: str, positions):
    pos = find(positions, symbol=symbol)
    return pos is not None and qty <= pos.qty


def check_owned_longs(user: UserDM, qty: int, symbol: str):
    return check_owned(qty, symbol, user.model.long_positions)


def check_owned_shorts(user: UserDM, qty: int, symbol: str):
    return check_owned(qty, symbol, user.model.short_positions)


def check_short_balance(user: UserDM, total_price: float):
    return total_price <= AccountStat(user).short_balance()
