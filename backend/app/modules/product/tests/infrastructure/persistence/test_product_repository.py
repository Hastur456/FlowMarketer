from decimal import Decimal
from uuid import uuid4

import pytest

from app.modules.product.domain.entities.product import Product
from app.modules.product.tests.factory import make_product


pytestmark = pytest.mark.asyncio


async def test_create_returns_domain_product(product_repository, db_session, category):
    product = make_product(category_id=category.id, name="Notebook", slug="notebook")

    created = await product_repository.create(product, session=db_session)

    assert isinstance(created, Product)
    assert created.id is not None
    assert created.name == "Notebook"
    assert created.slug == "notebook"
    assert created.gallery_urls == ["https://example.com/products/1.jpg"]


async def test_find_by_id_returns_product(product_repository, db_session, category):
    created = await product_repository.create(
        make_product(category_id=category.id),
        session=db_session,
    )

    found = await product_repository.find_by_id(created.id, session=db_session)

    assert found is not None
    assert isinstance(found, Product)
    assert found.id == created.id


async def test_find_by_id_returns_none_when_missing(product_repository, db_session):
    found = await product_repository.find_by_id(uuid4(), session=db_session)

    assert found is None


async def test_update_changes_product_fields(product_repository, db_session, category):
    created = await product_repository.create(
        make_product(category_id=category.id, price="100.00"),
        session=db_session,
    )

    updated = await product_repository.update(
        created.id,
        {"name": "Updated product", "price": Decimal("120.00")},
        session=db_session,
    )

    assert updated is not None
    assert updated.id == created.id
    assert updated.name == "Updated product"
    assert updated.price == Decimal("120.00")


async def test_update_returns_none_when_missing(product_repository, db_session):
    updated = await product_repository.update(
        uuid4(),
        {"name": "Missing"},
        session=db_session,
    )

    assert updated is None


async def test_delete_returns_deleted_product(product_repository, db_session, category):
    created = await product_repository.create(
        make_product(category_id=category.id),
        session=db_session,
    )

    deleted = await product_repository.delete(created.id, session=db_session)
    found = await product_repository.find_by_id(created.id, session=db_session)

    assert deleted is not None
    assert deleted.id == created.id
    assert found is None


async def test_find_active_returns_only_active_products(
    product_repository,
    db_session,
    category,
):
    active = await product_repository.create(
        make_product(category_id=category.id, is_active=True),
        session=db_session,
    )
    await product_repository.create(
        make_product(category_id=category.id, is_active=False),
        session=db_session,
    )

    result = await product_repository.find_active(session=db_session)

    assert [product.id for product in result] == [active.id]


async def test_find_featured_returns_only_active_featured_products(
    product_repository,
    db_session,
    category,
):
    featured = await product_repository.create(
        make_product(category_id=category.id, is_featured=True),
        session=db_session,
    )
    await product_repository.create(
        make_product(category_id=category.id, is_featured=False),
        session=db_session,
    )
    await product_repository.create(
        make_product(category_id=category.id, is_active=False, is_featured=True),
        session=db_session,
    )

    result = await product_repository.find_featured(session=db_session)

    assert [product.id for product in result] == [featured.id]


async def test_find_by_category_filters_active_products(
    product_repository,
    db_session,
    category,
):
    other_category = type(category)(name="Other category")
    db_session.add(other_category)
    await db_session.flush()

    expected = await product_repository.create(
        make_product(category_id=category.id),
        session=db_session,
    )
    await product_repository.create(
        make_product(category_id=category.id, is_active=False),
        session=db_session,
    )
    await product_repository.create(
        make_product(category_id=other_category.id),
        session=db_session,
    )

    result = await product_repository.find_by_category(
        category_id=category.id,
        session=db_session,
    )

    assert [product.id for product in result] == [expected.id]


async def test_find_by_price_range_filters_active_products(
    product_repository,
    db_session,
    category,
):
    expected = await product_repository.create(
        make_product(category_id=category.id, price="50.00"),
        session=db_session,
    )
    await product_repository.create(
        make_product(category_id=category.id, price="150.00"),
        session=db_session,
    )
    await product_repository.create(
        make_product(category_id=category.id, price="75.00", is_active=False),
        session=db_session,
    )

    result = await product_repository.find_by_price_range(
        min_price=Decimal("40.00"),
        max_price=Decimal("60.00"),
        session=db_session,
    )

    assert [product.id for product in result] == [expected.id]


async def test_update_stock_never_goes_below_zero(product_repository, db_session, category):
    created = await product_repository.create(
        make_product(category_id=category.id, stock_quantity=5),
        session=db_session,
    )

    updated = await product_repository.update_stock(
        product_id=created.id,
        quantity_change=-10,
        session=db_session,
    )

    assert updated is not None
    assert updated.stock_quantity == 0
