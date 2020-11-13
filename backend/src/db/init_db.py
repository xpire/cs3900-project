import csv
import logging
from os import path
from typing import Any

from sqlalchemy.orm import Session
from src.core.config import env_settings
from src.crud.crud_stock import stock
from src.db.session import SessionLocal, production_engine
from src.models import (
    LongPosition,
    Notification,
    ShortPosition,
    Stock,
    TimeSeries,
    UnlockedAchievement,
    User,
    WatchList,
)

metadatas = [
    User.metadata,
    Stock.metadata,
    TimeSeries.metadata,
    WatchList.metadata,
    LongPosition.metadata,
    UnlockedAchievement.metadata,
    ShortPosition.metadata,
    Notification.metadata,
]


def init_db(db: Session, is_test: bool, t_engine: Any) -> None:
    """Fill the stocks table with the selected stocks, also creates the database if it doesn't exist.

    Args:
        db (Session): database session
        is_test (bool): for pytest purposes
        t_engine (Any): testing engine
    """
    engine = t_engine if is_test else production_engine

    # create all tables
    for x in metadatas:
        x.create_all(bind=engine)

    print("Inserting initial stocks...")
    with open(path.join(str(env_settings.proj_root), "database", "stocks.csv"), mode="r") as file:
        reserved_stocks = [sd for sd in csv.DictReader(file)]
        stock.csv_batch_insert(db=db, csv_stocks=reserved_stocks)


if __name__ == "__main__":
    """
    Outer layer of initialization.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Create the initial data
    logger.info("Creating initial data")
    db = SessionLocal()
    init_db(db=db, is_test=False, t_engine=None)
    logger.info("Initial data created")
