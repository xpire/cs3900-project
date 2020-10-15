from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.src.core.config import settings

engine = create_engine(settings.SQLITE_DB_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)  # autocommit = False, autoflush = False


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
