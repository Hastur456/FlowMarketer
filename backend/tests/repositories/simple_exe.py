import pytest
from pydantic import BaseModel
from backend.app.repositories.postgres.base_repository import BaseRepository
from app.models.test_model import ExecutableModel


class ModelSchema(BaseModel):
    name: str
    slug: str


class Repository(BaseRepository[ExecutableModel]):
    model = ExecutableModel


@pytest.mark.asyncio
async def test_create(db_session):
    data = ModelSchema(name="string", slug="string")
    print(data)
    
    result = await Repository.create(data=data)
    print(f"Created: {result}")
    print(f"Name: {result.name}")

    assert result.name == "string"
    assert result.slug == "string"


@pytest.mark.asyncio
async def test_find_by_id(db_session):
    """Поиск по ID"""
    # ✅ Создаём модель вручную
    data = ModelSchema(name="Find", slug="find-me")
    obj = await Repository.create(data=data)
    
    found = await Repository.find_by_id(data_id=obj.id)
    
    assert found is not None
    assert found.id == obj.id
    assert found.name == "Find"


@pytest.mark.asyncio
async def test_find_all(db_session):
    """Получить все"""
    await Repository.create(data=ModelSchema(name="Product 1", slug="p1"))
    await Repository.create(data=ModelSchema(name="Product 2", slug="p2"))
    
    records = await Repository.find_all()
    
    assert len(records) == 2