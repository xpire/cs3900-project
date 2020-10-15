from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

# from backend.src.core.security import get_password_hash, verify_password
from backend.src.crud.base import CRUDBase
from backend.src.models.stock_data import StockData
from backend.src.schemas.stock_data import StockDataCreate, StockDataUpdate


class CRUDStockData(CRUDBase[StockData, StockDataCreate, StockDataUpdate]):
    def create(self, db: Session, *, obj_in: StockDataCreate) -> Optional[StockData]:
        pass


stockdata = CRUDStockData(StockData)