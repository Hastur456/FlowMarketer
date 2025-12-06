from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import func, TIMESTAMP, String
from uuid import uuid4
from datetime import datetime


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    create_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    update_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), server_onupdate=func.now()
    ) 

    @property
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
