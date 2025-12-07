# tests/repositories/test_base_repository.py
import pytest
from pydantic import BaseModel, Field, ConfigDict
from backend.app.repositories.postgres.base_repository import BaseRepository
from app.models.test_model import ExecutableModel


class ModelCreate(BaseModel):
    name: str
    slug: str


class ModelUpdate(BaseModel):
    name: str | None = Field(default=None)
    slug: str | None = Field(default=None)

    model_config = ConfigDict(
        from_attributes=True
    )


class ModelFilter(BaseModel):
    name: str | None = None


class ModelRepository(BaseRepository[ExecutableModel]):
    model = ExecutableModel


@pytest.mark.asyncio
async def test_create(db_session):
    """Создание записи"""
    data = ModelCreate(name="Product", slug="product-1")
    created = await ModelRepository.create(data=data)
    
    assert created.id is not None
    assert created.name == "Product"
    assert created.slug == "product-1"


@pytest.mark.asyncio
async def test_find_by_id(db_session):
    """Поиск по ID"""
    # ✅ Создаём модель вручную
    data = ModelCreate(name="Find", slug="find-me")
    obj = await ModelRepository.create(data=data)
    
    found = await ModelRepository.find_by_id(data_id=obj.id)
    
    assert found is not None
    assert found.id == obj.id
    assert found.name == "Find"


@pytest.mark.asyncio
async def test_find_by_id_not_found(db_session):
    """Поиск не найден"""
    found = await ModelRepository.find_by_id(data_id="fake-id-12345678")
    assert found is None


@pytest.mark.asyncio
async def test_find_all(db_session):
    """Получить все"""
    await ModelRepository.create(data=ModelCreate(name="Product 1", slug="p1"))
    await ModelRepository.create(data=ModelCreate(name="Product 2", slug="p2"))
    
    records = await ModelRepository.find_all()
    
    assert len(records) == 2


@pytest.mark.asyncio
async def test_find_all_empty(db_session):
    """Получить все из пустой БД"""
    records = await ModelRepository.find_all()
    assert len(records) == 0


@pytest.mark.asyncio
async def test_find_all_with_filter(db_session):
    """Получить с фильтром"""
    await ModelRepository.create(data=ModelCreate(name="Product A", slug="pa"))
    await ModelRepository.create(data=ModelCreate(name="Product B", slug="pb"))
    
    filters = ModelFilter(name="Product A")
    records = await ModelRepository.find_all(filters=filters)
    
    assert len(records) == 1
    assert records[-1].name == "Product A"


@pytest.mark.asyncio
async def test_update(db_session):
    """Обновление"""
    obj = await ModelRepository.create(data=ModelCreate(name="Old", slug="old"))
    
    data = ModelUpdate(name="New")
    updated = await ModelRepository.update(data_id=obj.id, data=data)
    
    assert updated.name == "New"
    assert updated.slug == "old"  # не изменилось


@pytest.mark.asyncio
async def test_update_not_found(db_session):
    """Обновление несуществующей"""
    data = ModelUpdate(name="New")
    updated = await ModelRepository.update(data_id="fake-id-12345678", data=data)
    assert updated is None


@pytest.mark.asyncio
async def test_delete(db_session):
    """Удаление"""
    obj = await ModelRepository.create(data=ModelCreate(name="Delete me", slug="delete"))
    
    deleted = await ModelRepository.delete(data_id=obj.id)
    
    assert deleted is True
    found = await ModelRepository.find_by_id(data_id=obj.id)
    assert found is None


@pytest.mark.asyncio
async def test_delete_not_found(db_session):
    """Удаление несуществующей"""
    deleted = await ModelRepository.delete(data_id="fake-id-12345678")
    assert deleted is False


@pytest.mark.asyncio
async def test_count(db_session):
    """Подсчет"""
    await ModelRepository.create(data=ModelCreate(name="P1", slug="p1"))
    await ModelRepository.create(data=ModelCreate(name="P2", slug="p2"))
    await ModelRepository.create(data=ModelCreate(name="P3", slug="p3"))
    
    count = await ModelRepository.count()
    assert count == 3


@pytest.mark.asyncio
async def test_count_with_filter(db_session):
    """Подсчет с фильтром"""
    await ModelRepository.create(data=ModelCreate(name="A", slug="a1"))
    await ModelRepository.create(data=ModelCreate(name="A", slug="a2"))
    await ModelRepository.create(data=ModelCreate(name="B", slug="b1"))
    
    filters = ModelFilter(name="A")
    count = await ModelRepository.count(filters=filters)
    assert count == 2


@pytest.mark.asyncio
async def test_exists_true(db_session):
    """Существует"""
    obj = await ModelRepository.create(data=ModelCreate(name="Exists", slug="exists"))
    
    exists = await ModelRepository.exists(data_id=obj.id)
    assert exists is True


@pytest.mark.asyncio
async def test_exists_false(db_session):
    """Не существует"""
    exists = await ModelRepository.exists(data_id="fake-id-12345678")
    assert exists is False
