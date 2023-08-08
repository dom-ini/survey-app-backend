from typing import Any

from sqlalchemy.orm import DeclarativeBase, declared_attr  # type: ignore[attr-defined]


class Base(DeclarativeBase):
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()
