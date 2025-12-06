from .base import Base 
from sqlalchemy import Column
from sqlalchemy.types import String


class TestModel(Base):
    __tablename__ = "test_model"
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, unique=True, index=True)
