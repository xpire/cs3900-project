import datetime as dt
import math
import random
from datetime import timedelta
from typing import Callable, Dict, List, Optional

import src.models as md
import src.schemas as sch
from randomtimestamp import randomtimestamp
from sqlalchemy.orm import Session
from src.core.config import settings
from src.core.utilities import log_msg
from src.db.base_model import BaseModel
from src.domain_models.order_dm import LimitOrder, Order
from src.domain_models.user_dm import UserDM
from src.models import all_models

from .utils import random_email, random_float, random_lower_string


def generate_random_user(*, is_init: bool) -> Dict:
    return {
        "uid": random_lower_string(length=(1, 128), rand_length=True),
        "email": random_email(),
        "username": random_lower_string(length=(1, 32), rand_length=True),  # longest user name be 32 characters
        "balance": 10000 if is_init else random_float(interval=(0, 1000000)),
        "level": 0 if is_init else random.randint(0, 10),
        "exp": 0 if is_init else random_float(interval=(0, 100)),
        "resets": 0 if is_init else random.randint(0, 10),
        "last_reset": dt.datetime.now() if is_init else randomtimestamp(start_year=dt.datetime.now().year, text=False),
    }


def generate_k_ranodm_users(*, init: int, k: int, shuffle: bool) -> Optional[List[Dict]]:
    """
    Generate k random users with init many initial users.
    """
    res = []
    if init <= k:
        for i in range(k):
            if init < k:
                res.append(generate_random_user(is_init=True))
            else:
                res.append(generate_random_user(is_init=False))
    else:
        log_msg("Please ensure that init <= k for user generation.")
        return None

    if shuffle:
        random.shuffle(res)
    return res


def set_db_state(
    *,
    db: Session,
    model: BaseModel,
    state: List[Dict],
) -> Optional[List[BaseModel]]:
    """
    Set up a state of database for testing purpose.
    Returns the list of model objects for use.
    """
    r = []
    if model in all_models:
        for s in state:
            db_obj = model(**s)
            db.add(db_obj)
            r.append(db_obj)

    try:
        db.commit()
        return r
    except:
        db.rollback()
        return None

    else:
        log_msg(f"Cannot add model {model.__class__} to database.", "ERROR")


def user_diff_checker(
    db: Session,
    test_users: List[Dict],
    checker: Callable,
):
    md_objs = set_db_state(db=db, model=md.User, state=test_users)
    user_dms = [UserDM(user_m=md, db=db) for md in md_objs]
    for dm, user in zip(user_dms, test_users):
        checker(dm=dm, user=user)


def get_mock_user():
    class MockUser:
        def __init__(self):
            self.level = 0

    return MockUser()


def get_test_order(Class, *args, **kwargs):

    return Class(*args, **kwargs)


def mock_return(value):
    def mock_return_value():
        return value

    return mock_return_value
