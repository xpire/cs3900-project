"""
Connects to the database
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from src.core.config import settings

production_engine = create_engine(settings.SQLITE_DB_URI, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=production_engine)  # autocommit = False, autoflush = False
SessionThreadLocal = scoped_session(SessionLocal)


def get_test_session():
    """
    Returns an instantiation of the current databse session
    """
    eng_test = create_engine(settings.SQLITE_TEST_DB_URI, connect_args={"check_same_thread": False})
    sesh_test = sessionmaker(bind=eng_test)
    return eng_test, sesh_test
