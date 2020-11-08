"""
Base schema for table creation - sets the table name
"""

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class BaseModel:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:  # Generate __tablename__ automatically
        return cls.__name__.lower()

    def dict(self):
        d = self.__dict__.copy()
        d.pop("_sa_instance_state", None)
        return d
