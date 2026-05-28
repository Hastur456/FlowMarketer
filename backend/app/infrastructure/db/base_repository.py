from abc import ABC
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.logger import logger
from app.infrastructure.db.mapper_interface import MapperInterface


DomainType = TypeVar("DomainType")
ModelType = TypeVar("ModelType")


class BaseRepository(
    ABC,
    Generic[DomainType, ModelType],
):
    model: type[ModelType] | None = None
    mapper: type[
        MapperInterface[DomainType, ModelType]
    ] | None = None

    def __init__(self, session: AsyncSession):
        self.session = session

    def _dump_data(self, data: BaseModel | dict) -> dict:
        return (
            data.model_dump(exclude_none=True)
            if isinstance(data, BaseModel)
            else data
        )

    async def find_by_id(
        self,
        data_id: str,
        session: AsyncSession | None = None,
    ):
        try:
            query = select(self.model).where(self.model.id == data_id)
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

    async def find_all(
        self,
        filters: BaseModel | None = None,
        session: AsyncSession | None = None
    ):
        filters_dict = filters.model_dump() if filters else {}

        try:
            query = select(self.model).filter_by(**filters_dict)
            response = await session.execute(query)
            records = response.scalars().all()

            logger.debug("Found %s records by filters %s", len(records), filters_dict)
            return records
        except SQLAlchemyError as error:
            logger.error("Error finding records by filters %s: %s", filters_dict, error)
            raise

    async def create(
        self,
        data: BaseModel | dict,
        session: AsyncSession | None = None,
    ):
        data_dict = self._dump_data(data)

        try:
            record = self.model(**data_dict)
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

    async def update(
        self,
        data_id: str,
        data: BaseModel | dict,
        session: AsyncSession | None = None,
    ):
        record = None

        try:
            query = select(self.model).where(self.model.id == data_id)
            response = await session.execute(query)
            record = response.scalar_one_or_none()

            if record is None:
                logger.warning("Record with id %s not found", data_id)
                return None

            instance = self._dump_data(data)

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

    async def delete(
        self,
        data_id: str,
        session: AsyncSession | None = None,
    ):
        try:
            query = select(self.model).where(self.model.id == data_id)
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

    async def count(
        self,
        filters: BaseModel | None = None,
        session: AsyncSession | None = None,
    ):
        filters_dict = filters.model_dump(exclude_unset=False) if filters else {}

        try:
            query = select(func.count()).select_from(self.model).filter_by(**filters_dict)
            response = await session.execute(query)
            return response.scalar_one_or_none()
        except SQLAlchemyError as error:
            logger.error("Error counting records by filters %s: %s", filters_dict, error)
            raise

    async def exists(
        self,
        data_id: str,
        session: AsyncSession | None = None,
    ):
        try:
            response = await self.find_by_id(data_id=data_id, session=session)

            if response is None:
                logger.warning("Record with id %s does not exist", data_id)
                return False

            return True
        except SQLAlchemyError as error:
            logger.error("Error checking record existence by id %s: %s", data_id, error)
            raise
