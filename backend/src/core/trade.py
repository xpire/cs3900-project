import src.api.endpoints.stocks as stocks_api
from sqlalchemy.orm import Session
from src.crud import crud_stock, crud_user
from src.domain_models.user_dm import UserDM


def get_stock_price(db: Session, symbol: str):
    return float(stocks_api.market_data_provider.data[symbol]["curr_day_close"])


def apply_commission(price: float, is_buying: bool = True):
    return price * 1.005 if is_buying else price * 0.995


def check_owned_longs(user: UserDM, qty: int, symbol: str):
    for position in user.model.long_positions:
        if position.symbol == symbol:
            return qty <= position.amount

    return False


def check_owned_shorts(user: UserDM, qty: int, symbol: str):
    for position in user.model.short_positions:
        if position.symbol == symbol:
            return qty <= position.amount

    return False


def check_short_balance(user: UserDM, total_price: float):
    return total_price <= user.get_short_balance()
