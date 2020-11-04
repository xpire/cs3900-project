from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.core.config import settings


def test_random_template(db: Session, client: TestClient):
    r = client.get("stocks/symbols")

    d = r.json()
    # INSERT MORE TESTS HERE
    assert r != None
    # assert r.status_code == 200
