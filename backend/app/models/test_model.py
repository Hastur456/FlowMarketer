from .base import Base 
from sqlalchemy import Column
from sqlalchemy.types import String


class ExecutableModel(Base):
    __tablename__ = "executable_model"
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=True, unique=True, index=True)
