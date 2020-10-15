from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from backend.src.crud.base import CRUDBase
from backend.src.models.stock import Stock
from backend.src.schemas.stock import StockCreate, StockUpdate


class CRUDStock(CRUDBase[Stock, StockCreate, StockUpdate]):
    def create_stock(
        self, db: Session, *, obj_in: StockCreate, owner_id: int
    ) -> Stock: 
        print('Creating Stock here.')
        pass

    # Please start implementing more of these functions, below are some sample to look at kek

    # def create_with_owner(
    #     self, db: Session, *, obj_in: ItemCreate, owner_id: int
    # ) -> Item:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data, owner_id=owner_id)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def get_multi_by_owner(
    #     self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    # ) -> List[Item]:
    #     return (
    #         db.query(self.model)
    #         .filter(Item.owner_id == owner_id)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )

stock = CRUDStock(Stock)
