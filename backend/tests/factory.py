# tests/factories.py
import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker
from tests.conftest import db_session

import pytest

from app.models.test_model import TestModel


fake = Faker()


class TestModelFactory(SQLAlchemyModelFactory):
    """Фабрика для создания тестовых моделей."""
    
    class Meta:
        model = TestModel
        # sqlalchemy_session будет установлена в фикстуре
        sqlalchemy_session_persistence = "flush"

    id = factory.LazyFunction(lambda: str(factory.Faker("uuid4")))
    name = factory.LazyAttribute(lambda obj: fake.word())
    slug = factory.LazyAttribute(lambda obj: fake.slug())
    created_at = factory.Faker("date_time_this_year")
    updated_at = factory.Faker("date_time_this_year")


@pytest.fixture
def test_model_factory(db_session):
    """Привязать фабрику к сессии."""
    TestModelFactory._meta.sqlalchemy_session = db_session
    return TestModelFactory
