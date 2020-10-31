import datetime
import random
from typing import Dict

import src.models as md
from fastapi.testclient import TestClient
from randomtimestamp import randomtimestamp
from sqlalchemy.orm import Session
from src.core.config import settings

from .utils import random_email, random_float, random_lower_string


def generate_random_user(is_init: bool) -> md.User:
    return {
        "uid": random_lower_string(l=(1, 128), rand_length=True),
        "email": random_email(),
        "username": random_lower_string(l=(1, 32), rand_length=True),  # longest user name be 32 characters
        "balance": 10000 if is_init else random_float(interval=(0, 1000000)),
        "level": 0 if is_init else random.randint(0, 10),
        "exp": 0 if is_init else random_float(interval=(0, 100)),
        "resets": 0 if is_init else random.randint(0, 10),
        "last_reset": datetime.datetime.now()
        if is_init
        else randomtimestamp(start_year=datetime.datetime.now().year, text=False),
    }


# Ignore the below code, just some useless code that might be useful later.

# user.add_transaction(db=ins, user_in=t_u, t_type="long", p_symbol="AAPL", p_amount=12, price=67.3)
# user.add_transaction(db=ins, user_in=t_u, t_type="long", p_symbol="AAPL", p_amount=12, price=67.3)
# user.add_transaction(db=ins, user_in=t_u, t_type="long", p_symbol="AAPL", p_amount=12, price=67.3)


# user.add_transaction(db=ins, user_in=t_u, t_type="short", p_symbol="AAPL", p_amount=12, price=67.3)
# user.add_transaction(db=ins, user_in=t_u, t_type="short", p_symbol="AAPL", p_amount=12, price=67.3)
# user.add_transaction(db=ins, user_in=t_u, t_type="short", p_symbol="AAPL", p_amount=12, price=67.3)


# user.deduct_transaction(db=ins, user_in=t_u, t_type="long", p_symbol="AAPL", p_amount=24)


# user.add_after_order(
#     db=ins,
#     user_in=t_u,
#     trade_type_in=TradeType.BUY,
#     amount_in=40,
#     symbol_in="AAPL",
#     dt_in=dt.now(),
# )

# user.add_after_order(
#     db=ins,
#     user_in=t_u,
#     trade_type_in=TradeType.BUY,
#     amount_in=30,
#     symbol_in="CBA",
#     dt_in=dt.now(),
# )

# user.add_after_order(
#     db=ins,
#     user_in=t_u,
#     trade_type_in=TradeType.BUY,
#     amount_in=50,
#     symbol_in="AAPL",
#     dt_in=dt.now(),
# )


# for x in t_u.transaction_hist:
#     print(x.__dict__)

# user.delete_after_order(db=ins, user_in=t_u, identity=1)
# user.delete_after_order(db=ins, user_in=t_u, identity=2)
# user.delete_after_order(db=ins, user_in=t_u, identity=3)
# user.add_history(db=ins, user_in=t_u, price_in=3.45, trade_type_in=TradeType.BUY, amount_in=34, symbol_in="AAPL")
# user.add_history(db=ins, user_in=t_u, price_in=6.75, trade_type_in=TradeType.SELL, amount_in=20, symbol_in="CBA")


# for x in t_u.transaction_hist:
#     print(x.__dict__)
