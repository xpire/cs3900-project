"""
Backend configuration settings for this project
"""
from os import path
from pathlib import Path
from typing import Any, List

import yaml

from firebase_admin import auth, credentials, initialize_app
from pydantic import AnyHttpUrl, BaseSettings

from .utilities import db_uri_generator, find_path_curr_f


class Settings(BaseSettings):
    PROJECT_NAME: str = "Xecute the Deal"
    DEV_NAME: str = "ecksdee"
    COURSE_NAME: str = "COMP3900"
    TD_API_KEY: str
    SQLITE_DB_URI: str
    SQLITE_TEST_DB_URI: str
    BACKEND_CORS_ORIGIN: List[AnyHttpUrl] = []
    FIRE_BASE_CRED: Any
    STARTING_BALANCE: float
    COMMISSION_RATE: float
    TIMEZONE: str
    RESET_WAIT_PERIOD_SECONDS: int


class LocalSettings(BaseSettings):
    # get secret path and needed paths
    abs_path: str = find_path_curr_f()[1]
    proj_src: Path = Path(abs_path).parent
    proj_backend: Path = proj_src.parent
    proj_root: Path = proj_backend.parent
    db_src: Path = proj_root / "database"


env_settings = LocalSettings()
settings = None
yaml_field = None

# Configure the firebase credentials
cred = credentials.Certificate(path.join(env_settings.abs_path, ".secrets", "ecksdee-firebase.json"))
initialize_app(cred)

# Configure the development environment
with open(path.join(env_settings.abs_path, ".secrets", "env.yaml")) as e:
    yaml_field = yaml.load(e, Loader=yaml.FullLoader)

    settings = Settings(
        PROJECT_NAME=yaml_field["PROJECT_NAME"],
        DEV_NAME=yaml_field["DEV_NAME"],
        COURSE_NAME=yaml_field["COURSE_NAME"],
        TD_API_KEY=yaml_field["TD_API_KEY"],
        SQLITE_DB_URI=db_uri_generator(proj_root=str(env_settings.proj_root), db_name=yaml_field["SQLITE_DB_NAME"]),
        SQLITE_TEST_DB_URI=db_uri_generator(
            proj_root=str(env_settings.proj_root), db_name=yaml_field["SQLITE_TEST_DB_NAME"]
        ),
        BACKEND_CORS_ORIGIN=[x for x in yaml_field["BACKEND_CORS_ORIGINS"]],
        FIRE_BASE_CRED=cred,
        STARTING_BALANCE=yaml_field["STARTING_BALANCE"],
        COMMISSION_RATE=yaml_field["COMMISSION_RATE"],
        TIMEZONE=yaml_field["TIMEZONE"],
        RESET_WAIT_PERIOD_SECONDS=yaml_field["RESET_WAIT_PERIOD_SECONDS"],
    )
