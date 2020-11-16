import functools
import random
import string
from typing import Any, Dict, Tuple

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.core.config import settings
from src.models import all_models


def random_lower_string(length: int, rand_length: bool) -> str:
    return "".join(
        random.choices(string.ascii_lowercase, k=random.randint(length[0], length[1]) if rand_length else length)
    )


def random_email() -> str:
    return f"{random_lower_string(length=(5, 20), rand_length=True)}@{random_lower_string(length=(5, 32), rand_length=True)}.com"


def random_float(interval: Tuple[float]) -> str:
    scaled = random.random()
    return interval[0] + scaled * abs(interval[1] - interval[0])


def clean_up(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        db = kwargs["db"]
        for m in all_models:
            try:
                num_rows_deleted = db.query(m).delete()
                db.commit()
            except:
                db.rollback()

    return wrapper
