# tests/repositories/test_base_repository.py
import pytest
from pydantic import BaseModel
from app.repositories.base_repository import BaseRepository
from app.models.test_model import TestModel


class TestModelCreate(BaseModel):
    name: str
    slug: str


class TestModelUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None


class TestModelFilter(BaseModel):
    name: str | None = None


class TestModelRepository(BaseRepository[TestModel]):
    model = TestModel


# ==================== ТЕСТЫ (БЕЗ ФАБРИКИ) ====================

@pytest.mark.asyncio
async def test_create():
    """Создание записи"""
    data = TestModelCreate(name="Product", slug="product-1")
    created = await TestModelRepository.create(data=data)
    
    assert created.id is not None
    assert created.name == "Product"
    assert created.slug == "product-1"


@pytest.mark.asyncio
async def test_find_by_id():
    """Поиск по ID"""
    # ✅ Создаём модель вручную
    data = TestModelCreate(name="Find", slug="find-me")
    obj = await TestModelRepository.create(data=data)
    
    found = await TestModelRepository.find_by_id(data_id=obj.id)
    
    assert found is not None
    assert found.id == obj.id
    assert found.name == "Find"


@pytest.mark.asyncio
async def test_find_by_id_not_found():
    """Поиск не найден"""
    found = await TestModelRepository.find_by_id(data_id="fake-id-12345678")
    assert found is None


@pytest.mark.asyncio
async def test_find_all():
    """Получить все"""
    await TestModelRepository.create(data=TestModelCreate(name="Product 1", slug="p1"))
    await TestModelRepository.create(data=TestModelCreate(name="Product 2", slug="p2"))
    
    records = await TestModelRepository.find_all()
    
    assert len(records) == 2


@pytest.mark.asyncio
async def test_find_all_empty():
    """Получить все из пустой БД"""
    records = await TestModelRepository.find_all()
    assert len(records) == 0


@pytest.mark.asyncio
async def test_find_all_with_filter():
    """Получить с фильтром"""
    await TestModelRepository.create(data=TestModelCreate(name="Product A", slug="pa"))
    await TestModelRepository.create(data=TestModelCreate(name="Product B", slug="pb"))
    
    filters = TestModelFilter(name="Product A")
    records = await TestModelRepository.find_all(filters=filters)
    
    assert len(records) == 1
    assert records.name == "Product A"


@pytest.mark.asyncio
async def test_update():
    """Обновление"""
    obj = await TestModelRepository.create(data=TestModelCreate(name="Old", slug="old"))
    
    data = TestModelUpdate(name="New")
    updated = await TestModelRepository.update(data_id=obj.id, data=data)
    
    assert updated.name == "New"
    assert updated.slug == "old"  # не изменилось


@pytest.mark.asyncio
async def test_update_not_found():
    """Обновление несуществующей"""
    data = TestModelUpdate(name="New")
    updated = await TestModelRepository.update(data_id="fake-id-12345678", data=data)
    assert updated is None


@pytest.mark.asyncio
async def test_delete():
    """Удаление"""
    obj = await TestModelRepository.create(data=TestModelCreate(name="Delete me", slug="delete"))
    
    deleted = await TestModelRepository.delete(data_id=obj.id)
    
    assert deleted is True
    found = await TestModelRepository.find_by_id(data_id=obj.id)
    assert found is None


@pytest.mark.asyncio
async def test_delete_not_found():
    """Удаление несуществующей"""
    deleted = await TestModelRepository.delete(data_id="fake-id-12345678")
    assert deleted is False


@pytest.mark.asyncio
async def test_count():
    """Подсчет"""
    await TestModelRepository.create(data=TestModelCreate(name="P1", slug="p1"))
    await TestModelRepository.create(data=TestModelCreate(name="P2", slug="p2"))
    await TestModelRepository.create(data=TestModelCreate(name="P3", slug="p3"))
    
    count = await TestModelRepository.count()
    assert count == 3


@pytest.mark.asyncio
async def test_count_with_filter():
    """Подсчет с фильтром"""
    await TestModelRepository.create(data=TestModelCreate(name="A", slug="a1"))
    await TestModelRepository.create(data=TestModelCreate(name="A", slug="a2"))
    await TestModelRepository.create(data=TestModelCreate(name="B", slug="b1"))
    
    filters = TestModelFilter(name="A")
    count = await TestModelRepository.count(filters=filters)
    assert count == 2


@pytest.mark.asyncio
async def test_exists_true():
    """Существует"""
    obj = await TestModelRepository.create(data=TestModelCreate(name="Exists", slug="exists"))
    
    exists = await TestModelRepository.exists(id=obj.id)
    assert exists is True


@pytest.mark.asyncio
async def test_exists_false():
    """Не существует"""
    exists = await TestModelRepository.exists(id="fake-id-12345678")
    assert exists is False
