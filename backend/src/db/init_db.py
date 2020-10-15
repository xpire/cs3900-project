from sqlalchemy.orm import Session


import csv
from backend.src import crud, schemas
from backend.src.crud.crud_stock import stock
from backend.src.core.config import settings
from backend.src.db import base  # noqa: F401
from backend.src.apis.api_util import get_db

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    # A = stock.get_stock_by_symbol(db=db, stock_symbol="TSLA")

    # # reserved_stocks = None
    print("Inserting stocks...")  # This
    with open("./src/db/stocks.csv", mode="r") as file:
        reserved_stocks = [sd for sd in csv.DictReader(file)]
        stock.csv_batch_insert(db=db, csv_stocks=reserved_stocks)
