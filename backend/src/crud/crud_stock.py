from typing import List, Optional, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from backend.src.crud.base import CRUDBase
from backend.src.models.stock import Stock
from backend.src.schemas.stock import StockCreate, StockUpdate
from backend.src.core.config import settings


class CRUDStock(CRUDBase[Stock, StockCreate, StockUpdate]):
    def get_stock_by_symbol(self, db: Session, stock_symbol: str) -> Optional[Stock]:
        """
        Get a single stock information
        """
        return db.query(self.model).filter(self.model.symbol == stock_symbol).first()

    def get_stock_by_symbols(
        self, db: Session, stock_symbols: List[str]
    ) -> Optional[List[Stock]]:
        """
        Get multiple stock information by multiple symbols.
        """
        return db.query(self.model).filter(self.model.symbol.in_(stock_symbols)).all()

    def csv_batch_insert(self, db: Session, csv_stocks: List[Dict]) -> Any:
        """
        Insert batch amount of basic stock data from existing model. Note that no type
        checks as the file is pretty much static.
        """
        ds = [dict(x) for x in csv_stocks]
        db.bulk_insert_mappings(self.model, ds)
        db.commit()
        return ds


stock = CRUDStock(Stock)
