import os
from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.core.config import env_settings, settings
from src.db.init_db import init_db
from src.db.session import get_test_session
from src.db.wake_db import init
from src.main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    engine, sesh = get_test_session()
    print("Setting up the testing environment...")
    init(is_test=True, test_session=sesh)  # wake_db
    init_db(db=sesh(), is_test=True, t_engine=engine)  # init db
    print("Cool...")
    yield sesh

    print("Testing environment tear down")
    t_db_path = env_settings.db_src / settings.SQLITE_TEST_DB_URI + ".sqlite3"
    if t_db_path.exists():
        os.remove(str(t_db_path))
    else:
        print("Missing testing db...")
    print("Cool...")


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
