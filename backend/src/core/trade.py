from src.domain_models.user_dm import UserDM
from src.crud import crud_user, crud_stock
from sqlalchemy.orm import Session


def get_stock_price(db: Session, symbol: str):
    # stock_obj = crud_stock.stock.get_stock_by_symbol(db, symbol)
    # return crud_stock.stock.get_time_series(db, stock_obj)[-1]
    return 100


def get_trade_price(price: float, quantity: int):
    return price * quantity


def apply_commission(price: float, buy: bool = True):
    return price * 1.005 if buy else price * 0.995


def check_owned_longs(user: UserDM, quantity: int, symbol: str):
    for position in user.model.portfolios:
        if position.symbol == symbol:
            return False if position.amount < quantity else True

    return False


def check_owned_shorts(user: UserDM, quantity: int, symbol: str):
    # for position in user.model.short_positions:
    #     if postion.symbol == symbol:
    #         return False if position.amount < quantity else True

    return True


def check_short_balance(user: UserDM, price: float):
    curr_shorts_owing = user.get_shorts_owing()
    curr_gross_portfolio_value = user.get_gross_portfolio_value()

    short_balance = curr_gross_portfolio_value * 0.25 - curr_shorts_owing
    
    return False if short_balance < price else True