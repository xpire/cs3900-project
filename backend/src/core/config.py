from os import path
from pathlib import Path
from typing import Any, List

import yaml
from fastapi import HTTPException
from firebase_admin import auth, credentials, initialize_app
from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, PostgresDsn, ValidationError, validator
from src.core.utilities import find_path_curr_f


class Settings(BaseSettings):
    PROJECT_NAME: str = "Xecute the Deal"
    DEV_NAME: str = "ecksdee"
    COURSE_NAME: str = "COMP3900"
    TD_API_KEY: str
    SQLITE_DB_URI: str
    BACKEND_CORS_ORIGIN: List[AnyHttpUrl] = []
    CRED_FB: Any


# get secret path and needed paths
_, abs_path = find_path_curr_f()

proj_src = Path(abs_path).parent
proj_backend_src = proj_src.parent
proj_root = proj_backend_src.parent

cred = credentials.Certificate(path.join(abs_path, ".secrets", "ecksdee-firebase.json"))
initialize_app(cred)

settings = None
with open(path.join(abs_path, ".secrets", "env.yaml")) as e:
    env = yaml.load(e, Loader=yaml.FullLoader)

    settings = Settings(
        PROJECT_NAME=env["PROJECT_NAME"],
        DEV_NAME=env["DEV_NAME"],
        COURSE_NAME=env["COURSE_NAME"],
        TD_API_KEY=env["TD_API_KEY"],
        SQLITE_DB_URI="sqlite:///" + path.join(str(proj_root), "database", env["SQLITE_DB_NAME"] + ".sqlite3"),
        SQLITE_TEST_DB_NAME="sqlite:///"
        + path.join(str(proj_root), "database", env["SQLITE_TEST_DB_NAME"] + ".sqlite3"),
        BACKEND_CORS_ORIGIN=[x for x in env["BACKEND_CORS_ORIGINS"]],
        CRED_FB=cred,
    )
