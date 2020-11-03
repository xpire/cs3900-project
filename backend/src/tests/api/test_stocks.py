from typing import Dict

from fastapi.testclient import TestClient
from src.core.config import settings


def test_random_template(client: TestClient):
    r = client.get("/stocks")

    d = r.json()
    # INSERT MORE TESTS HERE
    assert r != None
    assert r.status_code == 200
