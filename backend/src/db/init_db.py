import csv
import logging
from os import path

from sqlalchemy.orm import Session
from src.core.config import proj_root, settings
from src.crud.crud_stock import stock
from src.db import base_model_import_all as base_model  # noqa: F401
from src.db.base_model_import_all import (
    BaseModel,
    LongPosition,
    ShortPosition,
    Stock,
    TimeSeries,
    UnlockedAchievement,
    User,
    WatchList,
)
from src.db.session import SessionLocal, engine

metadatas = [
    User.metadata,
    Stock.metadata,
    TimeSeries.metadata,
    WatchList.metadata,
    LongPosition.metadata,
    UnlockedAchievement.metadata,
    ShortPosition.metadata,
]


def init_db(db: Session) -> None:
    """
    Fill the stocks table with the selected stocks, also creates
    the database if it doesn't exis
    """
    # create all tables
    for x in metadatas:
        x.create_all(bind=engine)

    print("Inserting initial stocks...")
    with open(path.join(str(proj_root), "database", "stocks.csv"), mode="r") as file:
        reserved_stocks = [sd for sd in csv.DictReader(file)]
        stock.csv_batch_insert(db=db, csv_stocks=reserved_stocks)


if __name__ == "__main__":
    """
    Out layer of initialization
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Create the initial data
    logger.info("Creating initial data")
    db = SessionLocal()
    init_db(db)
    logger.info("Initial data created")
