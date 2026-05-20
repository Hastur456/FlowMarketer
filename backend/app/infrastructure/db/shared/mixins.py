from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from uuid import UUID

from ..base import Base


class IdUUIDMixin(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True)
