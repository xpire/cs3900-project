import random
import string
from typing import Dict, Tuple

from fastapi.testclient import TestClient
from src.core.config import settings


def random_lower_string(length: int, rand_length: bool) -> str:
    return "".join(
        random.choices(string.ascii_lowercase, k=random.randint(length[0], length[1]) if rand_length else length)
    )


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string(l=32)}.com"


def random_float(interval: Tuple[float]) -> str:
    scaled = random.random()
    return interval[0] + scaled * abs(interval[1] - interval[0])
