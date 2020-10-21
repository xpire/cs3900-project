from src.models.user import User
from src.crud import crud_user, crud_stock
from sqlalchemy.orm import Session


def get_stock_price(db: Session, symbol: str):
    # stock_obj = crud_stock.stock.get_stock_by_symbol(db, symbol)
    # return crud_stock.stock.get_time_series(db, stock_obj)[-1]
    return 100


def get_trade_price(price: float, quantity: int, buy: bool = True):
    return price * quantity * 1.005 if buy else price * quantity * 0.995


def check_balance(user: User, price: float):
    return False if user.balance < price else True


def check_owned_stocks(user: User, quantity: int, symbol: str):
    for portfolio in user.portfolios:
        if portfolio.symbol == symbol:
            return True if portfolio.amount > quantity else False

    return False
