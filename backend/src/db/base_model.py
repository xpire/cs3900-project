from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class BaseModel:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:  # Generate __tablename__ automatically
        return cls.__name__.lower()

    def dict(self):
        # based on https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
