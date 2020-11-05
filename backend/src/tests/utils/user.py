import datetime
import random
from typing import Dict, List

import src.models as md
import src.schemas as sch
from fastapi.testclient import TestClient
from randomtimestamp import randomtimestamp
from sqlalchemy.orm import Session
from src.core.config import settings

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
        "last_reset": datetime.datetime.now()
        if is_init
        else randomtimestamp(start_year=datetime.datetime.now().year, text=False),
    }


def generate_k_ranodm_users(*, init: bool, k: int) -> List[Dict]:
    res = []
    for i in range(k):
        if init and i == 0:
            res.append(generate_random_user(is_init=init))
        else:
            res.append(generate_random_user(is_init=False))


def generate_k_create_schemas(*, k: int) -> List[sch.UserCreate]:
    res = []
    for i in range(k):
        temp = generate_random_user(is_init=True)
        res.append(
            sch.UserCreate(
                email=temp["email"],
                uid=temp["uid"],
                username=temp["username"],
            )
        )
    return res


# def insert_cheat_users(*, users: List[Dict]):
#     for u in users:
