from src.domain_models.user_dm import UserDM
from src.crud import crud_user, crud_stock
from sqlalchemy.orm import Session

import src.api.endpoints.stocks as stocks_api


def get_stock_price(db: Session, symbol: str):
    return float(stocks_api.latest_close_price_provider.data[symbol][0])


def apply_commission(price: float, buy: bool = True):
    return price * 1.005 if buy else price * 0.995


def check_owned_longs(user: UserDM, quantity: int, symbol: str):
    for position in user.model.long_positions:
        if position.symbol == symbol:
            return False if position.amount < quantity else True

    return False


def check_owned_shorts(user: UserDM, quantity: int, symbol: str):
    for position in user.model.short_positions:
        if position.symbol == symbol:
            return False if position.amount < quantity else True

    return False


def check_short_balance(user: UserDM, price: float):
    return False if user.get_short_balance() < price else True