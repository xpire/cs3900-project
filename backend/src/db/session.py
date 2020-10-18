from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

engine = create_engine(
    settings.SQLITE_DB_URI, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)  # autocommit = False, autoflush = False