from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.core.config import settings
from src.db.session import SessionLocal
from src.main import app
from src.tests.utils.user import authentication_token_from_email
from src.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()
    print("yeet")


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
