"""
CRUD operations for stocks
"""

from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from src.core.utilities import fail_save, log_msg
from src.crud.base import CRUDBase
from src.models.stock import Stock
from src.models.time_series import TimeSeries
from src.schemas.response import Fail, Result, return_result
from src.schemas.time_series import TimeSeriesDBcreate


class CRUDStock(CRUDBase[Stock]):
    def get_by_symbol(self, *, db: Session, symbol: str) -> Optional[Stock]:
        """Gets a single stock

        Args:
            db (Session): database session
            symbol (str): stock code

        Returns:
            Stock: stock object for the given symbol
        """
        return self.query(db).get(symbol)

    def get_multi_by_symbols(self, *, db: Session, symbols: List[str]) -> List[Stock]:
        """Gets multiple stocks

        Args:
            db (Session): database session
            symbols (List[str]): list of stock symbols

        Returns:
            List[Stock]: list of Stock objects for the given symbols
        """
        return self.query(db).filter(self.model.symbol.in_(symbols)).all()

    def symbol_exists(self, db: Session, symbol: str):
        """Checks if a stock symbol exists

        Args:
            db (Session): database session
            symbol (str): stock symbol

        Returns:
            Bool: True if symbol exists
        """
        return self.get_by_symbol(db=db, symbol=symbol) is not None

    def get_all_stocks(self, *, db: Session, simulated: Optional[bool] = None) -> List[Stock]:
        """Get all stock objects

        Args:
            db (Session): database session
            simulated (Optional[bool], optional): whether or not to return simulated stocks as well. Defaults to None.

        Returns:
            List[Stock]: List of stock objects for all stocks
        """
        if simulated is None:
            return self.query(db).all()
        elif simulated:
            return self.query(db).filter_by(industry="Simulated").all()
        else:
            return self.query(db).filter(self.model.industry != "Simulated").all()

    @fail_save
    def csv_batch_insert(self, *, db: Session, csv_stocks: List[Dict]) -> Any:
        """Fills database with information from csv, batch style. No type checks are done as the file is static.

        Returns:
            List[Dict]: list of dictionaries with csv rows
        """

        # wipe the table
        num_rows_deleted = db.query(Stock).delete()
        log_msg(f"{num_rows_deleted} rows deleted from stock table.", "INFO")

        ds = [dict(x) for x in csv_stocks]
        db.bulk_insert_mappings(self.model, ds)
        db.commit()
        return ds

    def get_time_series(self, *, db: Session, symbol: str, days: int) -> List[Dict]:
        """Get the sorted time series (historical data) of a stock. Returns most recent date first

        Returns:
            List[Dict]: list of historical data (open, close, etc.)
        """
        return db.query(TimeSeries).filter_by(symbol=symbol).order_by(TimeSeries.date.desc()).limit(days).all()

    @fail_save
    @return_result()
    def update_time_series(self, *, db: Session, symbol: str, time_series: List[TimeSeriesDBcreate]) -> Result:
        """Updates the time series information for a stock with the latest data

        Args:
            db (Session): database session
            symbol (str): stock symbol
            time_series (List[TimeSeriesDBcreate]): List of timeseries data for the stock

        Returns:
            Result: Success/Fail
        """
        stock = self.get_by_symbol(db=db, symbol=symbol)

        if stock.time_series.count() == 0:
            stock.time_series = [TimeSeries(**x.dict()) for x in time_series]

        else:
            latest_entry = max((x for x in stock.time_series), key=lambda x: x.date)

            for x in time_series:
                if symbol != x.symbol:
                    log_msg(f"Updating time series for {symbol} but entry for {time_series.symbol} passed in.")

                if x.date < latest_entry.date:
                    continue
                elif x.date == latest_entry.date:
                    latest_entry.__dict__.update(x.dict())
                else:
                    stock.time_series.append(TimeSeries(**x.dict()))
        db.commit()

    @fail_save
    def remove_all_hist(self, *, db: Session) -> None:
        """Deletes all time series data

        Args:
            db (Session): database session
        """
        try:
            num_rows_deleted = db.query(TimeSeries).delete()
            log_msg(f"{num_rows_deleted} rows cleared from timeseries.", "INFO")
            db.commit()
        except:
            log_msg("Error clearing historical data.", "ERROR")
            db.rollback()


stock = CRUDStock(Stock)
