from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

# from src.core.security import get_password_hash, verify_password
from src.crud.base import CRUDBase
from src.models.time_series import TimeSeries
from src.schemas.time_series import TimeSeriesCreate, TimeSeriesUpdate


class CRUDTimeSeries(CRUDBase[TimeSeries, TimeSeriesCreate, TimeSeriesUpdate]):
    def create(self, db: Session, *, obj_in: TimeSeriesCreate) -> Optional[TimeSeries]:
        pass


time_series = CRUDTimeSeries(TimeSeries)