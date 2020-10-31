from typing import Dict

from fastapi.testclient import TestClient
from src.core.config import settings


def random_test_template(client: TestClient):
    assert True == True
