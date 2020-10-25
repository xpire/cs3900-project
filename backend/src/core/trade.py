import src.api.endpoints.stocks as stocks_api
from sqlalchemy.orm import Session
from src.crud import crud_stock, crud_user


def get_stock_price(db: Session, symbol: str):
    return float(stocks_api.market_data_provider.data[symbol]["curr_day_close"])


def apply_commission(price: float, buy: bool = True):
    return price * 1.005 if buy else price * 0.995


def check_owned_longs(user, quantity: int, symbol: str):
    for position in user.model.long_positions:
        if position.symbol == symbol:
            return False if position.amount < quantity else True

    return False


def check_owned_shorts(user, quantity: int, symbol: str):
    for position in user.model.short_positions:
        if position.symbol == symbol:
            return False if position.amount < quantity else True

    return False


def check_short_balance(user, price: float):
    return False if user.get_short_balance() < price else True
