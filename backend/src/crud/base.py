"""
A base for CRUD operations.
"""


from typing import Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from src.db.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def query(self, db: Session):
        return db.query(self.model)

    def commit_and_refresh(self, db, obj):
        db.commit()
        db.refresh(obj)

    def create(self, db: Session, *, obj) -> ModelType:
        db_obj = self.model(**jsonable_encoder(obj))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
