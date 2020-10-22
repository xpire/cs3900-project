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
        Retieve the sorted time series of the obj_in.
        """
        # Need to reverse the order, since db returns in reverse order
        return [x.__dict__ for x in obj_in.timeseries][::-1]

    @fail_save
    def update_time_series(self, db: Session, obj_in: Stock, u_time_series: Dict) -> Stock:
        """
        Update the newest entry of time series. Update the value to u_time_series
        """
        tsc = None
        try:
            tsc = TimeSeriesCreate(
                datetime=u_time_series["datetime"],
                symbol=Stock.symbol,
                low=u_time_series["low"],
                high=u_time_series["high"],
                open=u_time_series["open"],
                close=u_time_series["close"],
                volume=u_time_series["volume"],
            )
        except ValidationError as e:
            log_msg(f"Failed to update time series {u_time_series.__str__}.", "ERROR")
            return obj_in

        # BUG: Below could be computationally expensive, optimize later maybe
        tsc = TimeSeries(**tsc.dict())

        l = len(obj_in.timeseries)
        newest = obj_in.timeseries[l]
        obj_in.timeseries.remove(newest)
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
                # @Even Tang
                # Change this later
                # dt = datetime.strptime(row["datetime"], "%Y-%m-%d")
                # dt_str = dt.strftime("%Y-%m-%d")
                # dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                # print(dt.strftime("%Y-%m-%d %H:%M:%S"))
                tsc = TimeSeriesCreate(
                    datetime=row["datetime"],
                    symbol=obj_in.symbol,
                    low=row["low"],
                    high=row["high"],
                    open=row["open"],
                    close=row["close"],
                    volume=row["volume"],
                )

                # Check if currently exists
                entry = (
                    db.query(TimeSeries)
                    .filter(and_(TimeSeries.datetime == row["datetime"], TimeSeries.symbol == obj_in.symbol))
                    .first()
                )

                tsc = TimeSeries(**tsc.dict())
                # print(tsc.__dict__)
                if entry:
                    entry = tsc  # Replace if found
                else:
                    obj_in.timeseries.append(tsc)  # Otherwise, add row

            except ValidationError as e:
                log_msg(f"Failed to insert time series {row.__str__}.", "ERROR")
                continue

        db.commit()
        db.refresh(obj_in)

        return obj_in


stock = CRUDStock(Stock)
