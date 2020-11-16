import os
from typing import Dict, Generator

import pytest
from sqlalchemy.orm import Session
from src.core.config import env_settings, settings, yaml_field
from src.db.init_db import init_db
from src.db.session import get_test_session
from src.db.wake_db import init


@pytest.fixture(scope="session")
def db() -> Generator:
    engine, sesh = get_test_session()
    print("Setting up the testing environment...")
    init(is_test=True, test_session=sesh())  # wake_db
    init_db(db=sesh(), is_test=True, t_engine=engine)  # init db
    print("Cool...")
    yield sesh()
    print("Testing environment tear down")
    t_db_path = str(env_settings.db_src / yaml_field["SQLITE_TEST_DB_NAME"]) + ".sqlite3"
    if os.path.exists(t_db_path):
        os.remove(str(t_db_path))
        print("Cool...")
    else:
        print("Missing testing db...")
