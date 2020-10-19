from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any


@as_declarative()
class BaseModel:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:  # Generate __tablename__ automatically
        return cls.__name__.lower()
