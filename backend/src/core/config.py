from typing import List, Union
from decouple import config

from pydantic import (
    BaseSettings,
    AnyHttpUrl,
    ValidationError,
    validator,
)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Xecute the Deal"
    DEV_NAME: str = "ecksdee"
    COURSE_NAME: str = "COMP3900"
    TD_API_KEY: str

    SQLITE_DB_URI: str
    BACKEND_CORS_ORIGIN: List[AnyHttpUrl] = []


# Read things from here
settings = Settings(
    PROJECT_NAME=config("PROJECT_NAME"),
    DEV_NAME=config("DEV_NAME"),
    COURSE_NAME=config("COURSE_NAME"),
    TD_API_KEY=config("TD_API_KEY"),
    SQLITE_DB_URI=config("SQLITE_DB_URI"),
    BACKEND_CORS_ORIGIN=[
        str(x) for x in config("BACKEND_CORS_ORIGINS")[1:-1].split(", ")
    ],
)