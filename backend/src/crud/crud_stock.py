import json
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import ValidationError
from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.core.config import settings
from src.core.utilities import fail_save, log_msg
from src.crud.base import CRUDBase
from src.models.stock import Stock
from src.models.time_series import TimeSeries
from src.schemas.stock import StockCreate, StockUpdate
from src.schemas.time_series import TimeSeriesCreate


class CRUDStock(CRUDBase[Stock, StockCreate, StockUpdate]):
    def get_stock_by_symbol(self, db: Session, stock_symbol: str) -> Optional[Stock]:
        """
        Get a single stock information
        """
        return db.query(self.model).filter(self.model.symbol == stock_symbol).first()

    def get_stock_by_symbols(self, db: Session, stock_symbols: List[str]) -> Optional[List[Stock]]:
        """
        Get multiple stock information by multiple symbols.
        """
        return db.query(self.model).filter(self.model.symbol.in_(stock_symbols)).all()

    def get_all_stocks(self, db: Session) -> Optional[List[Stock]]:
        """
        Get multiple stock information by multiple symbols.
        """
        return db.query(self.model).all()

    @fail_save
    def csv_batch_insert(self, db: Session, csv_stocks: List[Dict]) -> Any:
        """
        Insert batch amount of basic stock data from existing model. Note that no type
        checks as the file is pretty much static.
        """
        ds = [dict(x) for x in csv_stocks]
        db.bulk_insert_mappings(self.model, ds)
        db.commit()
        return ds

    def get_time_series(self, db: Session, obj_in: Stock) -> List[Optional[Dict]]:
        """
        Retieve the sorted time series of the obj_in. Returns latest date first.
        """
        # Need to reverse the order, since db returns in reverse order
        return [x.__dict__ for x in obj_in.timeseries][::-1]

    @fail_save
    def update_time_series(self, db: Session, obj_in: Stock, u_time_series: Dict) -> Stock:
        """
        Update the newest entry of time series. Update last 2 entries u_time_series.
        """

        # only 2 entries
        for e in u_time_series:
            tsc = None
            try:
                tsc = TimeSeriesCreate(
                    date=e["datetime"],
                    symbol=obj_in.symbol,
                    low=e["low"],
                    high=e["high"],
                    open=e["open"],
                    close=e["close"],
                    volume=e["volume"],
                )
            except ValidationError as e:
                log_msg(f"Failed to update time series {e.__str__}.", "ERROR")
                return obj_in

            tsc = TimeSeries(**tsc.dict())

            found = False
            for t in obj_in.timeseries:
                if t.date == tsc.date:
                    found = True
                    t.low = tsc.low
                    t.high = tsc.high
                    t.open = tsc.open
                    t.close = tsc.close

            if not found:
                obj_in.timeseries.append(tsc)

        db.commit()
        db.refresh(obj_in)

        return obj_in

    @fail_save
    def batch_add_daily_time_series(self, db: Session, obj_in: Stock, time_series_in: List[Dict]) -> Stock:
        """
        Batch insert historical daily timeseries candle stock data, continue insertion even
        if 1 entry fails convention.
        """
        for row in time_series_in:
            tsc = None
            try:
                tsc = TimeSeriesCreate(
                    date=row["datetime"],
                    symbol=obj_in.symbol,
                    low=row["low"],
                    high=row["high"],
                    open=row["open"],
                    close=row["close"],
                    volume=row["volume"],
                )

                tsc = TimeSeries(**tsc.dict())
                obj_in.timeseries.append(tsc)  # Otherwise, add row

            except ValidationError as e:
                log_msg(f"Failed to insert time series {row.__str__}.", "ERROR")
                continue

        db.commit()
        db.refresh(obj_in)

        return obj_in

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
