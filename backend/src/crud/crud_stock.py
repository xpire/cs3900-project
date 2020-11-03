from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from src.core.config import settings
from src.core.utilities import fail_save, log_msg
from src.crud.base import CRUDBase
from src.models.stock import Stock
from src.models.time_series import TimeSeries
from src.schemas.response import Fail, Result, return_result
from src.schemas.time_series import TimeSeriesDBcreate


class CRUDStock(CRUDBase[Stock]):
    def get_stock_by_symbol(self, *, db: Session, symbol: str) -> Optional[Stock]:
        """
        Get a single stock
        """
        return self.query(db).get(symbol)

    def get_stock_by_symbols(self, *, db: Session, symbols: List[str]) -> List[Stock]:
        """
        Get multiple stock by multiple symbols.
        """
        return self.query(db).filter(self.model.symbol.in_(symbols)).all()

    def symbol_exists(self, db: Session, symbol: str):
        """
        Return True if the symbol exists
        """
        return self.get_stock_by_symbol(db=db, symbol=symbol) is not None

    def get_all_stocks(self, *, db: Session) -> List[Stock]:
        """
        Get all stock objects
        """
        return self.query(db).all()

    @fail_save
    def csv_batch_insert(self, *, db: Session, csv_stocks: List[Dict]) -> Any:
        """
        Insert batch amount of basic stock data from existing model. Note that no type
        checks as the file is pretty much static.
        """
        ds = [dict(x) for x in csv_stocks]
        db.bulk_insert_mappings(self.model, ds)
        db.commit()
        return ds

    def get_time_series(self, *, db: Session, symbol: str, days: int) -> List[Dict]:
        """
        Retieve the sorted time series of the obj. Returns latest date first
        """
        return db.query(TimeSeries).filter_by(symbol=symbol).order_by(TimeSeries.date.desc()).limit(days).all()

    @fail_save
    @return_result()
    def update_time_series(self, *, db: Session, symbol: str, time_series: List[TimeSeriesDBcreate]) -> Result:
        """
        Update the newest entry of time series
        """
        stock = self.get_stock_by_symbol(db=db, symbol=symbol)

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

    '''
    @fail_save
    @return_result()
    def update_time_series(self, *, db: Session, timeseries: List[TimeSeriesCreate]) -> Result:
        """
        Update the newest entry of time series. Update last 2 entries u_time_series.
        """
        for x in timeseries:
            db_obj = db.query(TimeSeries).get((x.date, x.symbol))
            if db_obj is None:
                db.add(TimeSeries(**x.dict()))
            else:
                db_obj.__dict__.update(x.dict())
        db.commit()

    # TODO if above works well, remove below
    @fail_save
    def batch_add_daily_time_series(self, *, db: Session, stock: Stock, time_series: List[Dict]) -> Stock:
        """
        Batch insert historical daily timeseries candle stock data, continue insertion even
        if 1 entry fails convention.
        """
        # https://stackoverflow.com/questions/7133007/sqlalchemy-get-max-min-avg-values-from-a-table
        # TODO: get latest entry and add on the rest
        # except, for the day where it collides, update, since it may be intraday
        for row in time_series:
            attempt_entry = None
            try:
                attempt_entry = TimeSeriesCreate(
                    date=row["datetime"],
                    symbol=stock.symbol,
                    low=row["low"],
                    high=row["high"],
                    open=row["open"],
                    close=row["close"],
                    volume=row["volume"],
                )

                attempt_entry = TimeSeries(**attempt_entry.dict())
                stock.timeseries.append(attempt_entry)  # Otherwise, add row

            except ValidationError as e:
                log_msg(f"Failed to insert time series {row.__str__}.", "ERROR")
                continue

        self.commit_and_refresh(db, stock)
        return stock
    '''

    @fail_save
    def remove_all_hist(self, *, db: Session) -> None:
        try:
            num_rows_deleted = db.query(TimeSeries).delete()
            log_msg(f"{num_rows_deleted} rows cleared from timeseries.", "INFO")
            db.commit()
        except:
            log_msg("Error clearing historical data.", "ERROR")
            db.rollback()


stock = CRUDStock(Stock)
