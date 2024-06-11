from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        if cls.__name__.endswith("s"):
            return cls.__name__.lower() + "es"
        else:
            return cls.__name__.lower() + "s"
