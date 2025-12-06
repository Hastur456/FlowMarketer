from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from pydantic import BaseModel

from app.database.session import connection
from app.utils.logger import logger
from typing import Generic, TypeVar


T = TypeVar("T")


class BaseRepository(Generic[T]):
    model: type[T] = None


    @classmethod
    @connection(commit=False)
    async def find_by_id(cls, session: AsyncSession, data_id: str):
        try:
            query = select(cls.model).filter_by(data_id)
            
            response = await session.execute(query)
            record = response.scalar_one_or_none()

            if not (record is None):
                logger.debug("Найдена запись {}, по id {data_id}".format(record, data_id))
                return record
            else:
                logger.debug("Запись с id: {}, не найдена".format(data_id))
                return None
        except SQLAlchemyError as e:
            logger.error("Ошибка при поиске по id {}, error: {}".format(data_id, e))
            raise


    @classmethod
    @connection(commit=False)
    async def find_all(cls, session: AsyncSession, filters: BaseModel | None = None):        
        try:
            filters_dict = filters.model_dump() if filters else {}

            query = select(cls.model).filter_by(**filters_dict)
            response = await session.execute(query)
            records = response.scalars().all()

            logger.debug("Найдено {} записей, по фильтрам {}".format(len(records), filters_dict))
            return records
        except SQLAlchemyError as e:
            logger.error("Ошибка при поиске по фильтрам {}, error: {}".format(filters_dict, e))
            raise


    @classmethod
    @connection(commit=True)
    async def create(cls, session: AsyncSession, data: BaseModel):
        try:
            data_dict = data.model_dump()
            template = cls.model(**data_dict)

            session.add(template)
            await session.flush()

        except SQLAlchemyError as e:
            logger.error("Ошибка при выполнении добавлении в базу даннх объекта: {}, ошибка: {}".format(data_dict, e))

    
    @classmethod
    @connection(commit=True)
    async def update(cls, session: AsyncSession, data_id: str, data: BaseModel):
        try:
            query = select(cls.model).where(cls.model.id == data_id)
            response = await session.execute(query)
            record = response.scalar_one_or_none()

            instance = data.model_dump(exclude_unset=False)

            if instance is None:
                logger.warning("Данные для изменения не добавлены.")
                return None

            for key, value in instance.items():
                if hasattr(record, key):
                    record[key] = value

            session.add(instance)
            await session.flush()

            logger.info("Данные с ID {} изменены".format(data_id))

            return record
        
        except SQLAlchemyError as e:
            logger.error("Ошибка при обновлении данных объекта: {}, ошибка: {}".format(record, e))
            raise
        
    
    @classmethod
    @connection(commit=True)
    async def delete(cls, session: AsyncSession, data_id: str):
        try:
            query = select(cls.model).where(cls.mdoel.id == data_id)
            request = await session.execute(query)
            record = request.scalar_one_or_none()

            session.delete(record)
            await session.flush()

        except SQLAlchemyError as e:
            logger.error("Ошибка при удалении данных с ID: {}, ошибка: {}".format(data_id, e))
            raise

    
    @classmethod
    @connection(commit=False)
    async def count(cls, session: AsyncSession, filters: BaseModel | None = None):
        try:
            filters_dict = filters.model_dump(exclude_unset=False) if filters else {}

            query = select(func.count()).select_from(cls.model).filter_by(**filters_dict)
            response = await session.execute(query)

            total_count = response.scalar_one_or_none()

            return total_count
        
        except SQLAlchemyError as e:
            logger.error("Ошибка при получении количества объектов по фильтрам {}, ошибка: {}".format(filters_dict, e))
            raise
