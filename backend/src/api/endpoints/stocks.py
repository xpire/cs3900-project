from typing import List

from fastapi import Depends, Query
from sqlalchemy.orm import Session
from src import crud
from src import domain_models as dm
from src import schemas
from src.api import common
from src.api.deps import check_symbol, get_db
from src.domain_models.trading_hours import trading_hours_manager
from src.schemas.response import RaiseFail, ResultAPIRouter
from src.schemas.stock import StockAPIout

router = ResultAPIRouter()


@router.get("/")
async def get_symbols(db: Session = Depends(get_db)) -> List[StockAPIout]:
    """API endpoint to get full list of stocks

    Args:
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        List[StockAPIout]: List of stock information for all stocks in database
    """
    return crud.stock.get_multi_by_symbols(db=db, symbols=dm.get_data_provider().symbols)


@router.get("/real_time")
async def get_stocks(
    symbols: List[str] = Query(None), db: Session = Depends(get_db)
) -> List[schemas.StockRealTimeAPIout]:
    """API endpoint to get the realtime data for a list of provided stockss

    Args:
        symbols (List[str], optional): list of stock symbols real time data is needed for. Defaults to Query(None).
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        List[schemas.StockRealTimeAPIout]: realtime data updates for each stock symbol
    """
    if not symbols:
        return []

    stocks = crud.stock.get_multi_by_symbols(db=db, symbols=symbols)
    if len(stocks) != len(symbols):
        RaiseFail(f"Following symbols are requested but do not exist: {set(symbols) - set(stocks)}")

    return [common.stock_to_realtime_schema(stock) for stock in stocks]


@router.get("/real_time/all")
async def get_stocks(db: Session = Depends(get_db)) -> List[schemas.StockRealTimeAPIout]:
    """API endpoint to get the realtime data for all stocks

    Args:
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        List[schemas.StockRealTimeAPIout]: realtime data updates for all stocks
    """
    stocks = crud.stock.get_multi_by_symbols(db=db, symbols=dm.get_data_provider().symbols)
    return [common.stock_to_realtime_schema(stock) for stock in stocks]


@router.get("/time_series")
async def get_stock_data(
    symbol: str = Depends(check_symbol), db: Session = Depends(get_db), days: int = 90
) -> List[schemas.TimeSeriesAPIout]:
    """API enpoint to get the historical data of a stock

    Args:
        symbol (str, optional): stock symbol. Defaults to Depends(check_symbol).
        db (Session, optional): database session. Defaults to Depends(get_db).
        days (int, optional): Number of days worth of historical data that is requested. Defaults to 90.

    Returns:
        List[schemas.TimeSeriesAPIout]: time series historical data for the stock
    """
    return crud.stock.get_time_series(db=db, symbol=symbol, days=days)


@router.get("/trading_hours")
async def get_trading_hours(
    symbol: str = Depends(check_symbol), db: Session = Depends(get_db)
) -> schemas.TradingHoursInfo:
    """API endpoint to get the trading hours of a particular stock

    Args:
        symbol (str, optional): stock symbol. Defaults to Depends(check_symbol).
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        schemas.TradingHoursInfo: trading hours of the stock
    """
    stock = crud.stock.get_by_symbol(db=db, symbol=symbol)
    return trading_hours_manager.get_trading_hours_info(stock)
