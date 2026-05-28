from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.logger import logger


T = TypeVar("T")


class BaseRepository(Generic[T]):
    model: type[T] = None

    @staticmethod
    def _dump_data(data: BaseModel | dict) -> dict:
        return data.model_dump() if isinstance(data, BaseModel) else data

    @classmethod
    async def find_by_id(
        cls,
        data_id: str,
        session: AsyncSession | None = None,
    ):
        try:
            query = select(cls.model).where(cls.model.id == data_id)
            response = await session.execute(query)
            record = response.scalar_one_or_none()

            if record:
                logger.info("Found record %s by id %s", record, data_id)
                return record

            logger.info("Record with id %s not found", data_id)
            return None
        except SQLAlchemyError as error:
            logger.error("Error finding record by id %s: %s", data_id, error)
            raise

    @classmethod
    async def find_all(
        cls,
        filters: BaseModel | None = None,
        session: AsyncSession | None = None
    ):
        filters_dict = filters.model_dump() if filters else {}

        try:
            query = select(cls.model).filter_by(**filters_dict)
            response = await session.execute(query)
            records = response.scalars().all()

            logger.debug("Found %s records by filters %s", len(records), filters_dict)
            return records
        except SQLAlchemyError as error:
            logger.error("Error finding records by filters %s: %s", filters_dict, error)
            raise

    @classmethod
    async def create(
        cls,
        data: BaseModel | dict,
        session: AsyncSession | None = None,
    ):
        data_dict = cls._dump_data(data)

        try:
            record = cls.model(**data_dict)
            session.add(record)
            await session.flush()
            await session.refresh(record)
            await session.commit()

            logger.info("Created record: %s", data)
            return record
        except SQLAlchemyError as error:
            await session.rollback()
            logger.error("Error creating record %s: %s", data_dict, error)
            raise

    @classmethod
    async def update(
        cls,
        data_id: str,
        data: BaseModel | dict,
        session: AsyncSession | None = None,
    ):
        record = None

        try:
            query = select(cls.model).where(cls.model.id == data_id)
            response = await session.execute(query)
            record = response.scalar_one_or_none()

            if record is None:
                logger.warning("Record with id %s not found", data_id)
                return None

            instance = cls._dump_data(data)

            if instance is None:
                logger.warning("No update data provided")
                return None

            for key, value in instance.items():
                if hasattr(record, key) and value is not None:
                    setattr(record, key, value)

            await session.flush()
            await session.refresh(record)
            await session.commit()

            logger.info("Updated record with id %s", data_id)
            return record
        except SQLAlchemyError as error:
            await session.rollback()
            logger.error("Error updating record %s: %s", record, error)
            raise

    @classmethod
    async def delete(
        cls,
        data_id: str,
        session: AsyncSession | None = None,
    ):
        try:
            query = select(cls.model).where(cls.model.id == data_id)
            request = await session.execute(query)
            record = request.scalar_one_or_none()

            if record is None:
                logger.warning("Record with id %s not found", data_id)
                return False

            await session.delete(record)
            await session.flush()
            await session.commit()

            return True
        except SQLAlchemyError as error:
            await session.rollback()
            logger.error("Error deleting record with id %s: %s", data_id, error)
            raise

    @classmethod
    async def count(
        cls,
        filters: BaseModel | None = None,
        session: AsyncSession | None = None,
    ):
        filters_dict = filters.model_dump(exclude_unset=False) if filters else {}

        try:
            query = select(func.count()).select_from(cls.model).filter_by(**filters_dict)
            response = await session.execute(query)
            return response.scalar_one_or_none()
        except SQLAlchemyError as error:
            logger.error("Error counting records by filters %s: %s", filters_dict, error)
            raise

    @classmethod
    async def exists(
        cls,
        data_id: str,
        session: AsyncSession | None = None,
    ):
        try:
            response = await cls.find_by_id(data_id=data_id, session=session)

            if response is None:
                logger.warning("Record with id %s does not exist", data_id)
                return False

            return True
        except SQLAlchemyError as error:
            logger.error("Error checking record existence by id %s: %s", data_id, error)
            raise
