from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import crud
from src import domain_models as dm
from src import schemas
from src.api.deps import check_symbol, get_db
from src.domain_models.trading_hours import trading_hours_manager
from src.schemas.response import RaiseFail
from src.schemas.stock import StockAPIout

router = APIRouter()


@router.get("/")
async def get_symbols(db: Session = Depends(get_db)) -> List[StockAPIout]:
    return crud.stock.get_multi_by_symbols(db=db, symbols=dm.get_data_provider().symbols)


@router.get("/real_time")
async def get_stocks(
    symbols: List[str] = Query(None), db: Session = Depends(get_db)
) -> List[schemas.StockRealTimeAPIout]:
    if not symbols:
        return []

    stocks = crud.stock.get_multi_by_symbols(db=db, symbols=symbols)
    if len(stocks) != len(symbols):
        RaiseFail(f"Following symbols are requested but do not exist: {set(symbols) - set(stocks)}")

    def to_schema(stock):
        return schemas.StockRealTimeAPIout(
            **stock.dict(),
            **dm.get_data_provider().data[stock.symbol],
            trading_hours_info=trading_hours_manager.get_trading_hours_info(stock),
        )

    return [to_schema(stock) for stock in stocks]


@router.get("/time_series")
async def get_stock_data(
    symbol: str = Depends(check_symbol), db: Session = Depends(get_db), days: int = 90
) -> List[schemas.TimeSeriesAPIout]:
    return crud.stock.get_time_series(db=db, symbol=symbol, days=days)


@router.get("/trading_hours")
async def get_trading_hours(symbol: str = Depends(check_symbol), db: Session = Depends(get_db)):  # TODO define schema
    stock = crud.stock.get_by_symbol(db=db, symbol=symbol)
    return trading_hours_manager.get_trading_hours_info(stock)
