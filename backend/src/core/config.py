from typing import List
from decouple import config

from pydantic import BaseSettings, PostgresDsn, AnyHttpUrl

class Settings(BaseSettings):
    PROJECT_NAME: str = "Xecute the Deal"
    DEV_NAME: str = "ecksdee"
    COURSE_NAME: str = "COMP3900"
    
    TW_API_KEY: str 
    FH_API_KEY: str

    SQLALCHEMY_DATABASE_URI: PostgresDsn
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

# Read things from here
settings = Settings(
    PROJECT_NAME = config("PROJECT_NAME"), 
    DEV_NAME = config("DEV_NAME"), 
    COURSE_NAME = config("COURSE_NAME"), 
    TW_API_KEY = config("TW_API_KEY"), 
    FH_API_KEY = config("FH_API_KEY"), 
    SQLALCHEMY_DATABASE_URI = config("SQLALCHEMY_DATABASE_URI"), 
    BACKEND_CORS_ORIGINS = [str(x) for x in config("BACKEND_CORS_ORIGINS")[1:-1].split(", ")]
)