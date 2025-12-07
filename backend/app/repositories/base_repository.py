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
            query = select(cls.model).where(cls.model.id == data_id)
            
            response = await session.execute(query)
            record = response.scalar_one_or_none()

            if not (record is None):
                logger.info("Найдена запись {}, по id {}".format(record, data_id))
                return record
            else:
                logger.info("Запись с id: {}, не найдена".format(data_id))
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
            logger.info(f"Объект успешно создан: {data}")
            return template
        except SQLAlchemyError as e:
            logger.error("Ошибка при выполнении добавлении в базу даннх объекта: {}, ошибка: {}".format(data_dict, e))

    
    @classmethod
    @connection(commit=True)
    async def update(cls, session: AsyncSession, data_id: str, data: BaseModel):
        try:
            query = select(cls.model).where(cls.model.id == data_id)
            response = await session.execute(query)
            record = response.scalar_one_or_none()

            if record is None:
                logger.warning("Объект с ID {} не найден".format(data_id))
                return None

            instance = data.model_dump(exclude_unset=False)

            if instance is None:
                logger.warning("Данные для изменения не добавлены.")
                return None

            for key, value in instance.items():
                if hasattr(record, key) and value is not None:
                    setattr(record, key, value)

            await session.flush()
            await session.refresh(record)

            logger.info("Данные с ID {} изменены".format(data_id))

            return record
        
        except SQLAlchemyError as e:
            logger.error("Ошибка при обновлении данных объекта: {}, ошибка: {}".format(record, e))
            raise
        
    
    @classmethod
    @connection(commit=True)
    async def delete(cls, session: AsyncSession, data_id: str):
        try:
            query = select(cls.model).where(cls.model.id == data_id)
            request = await session.execute(query)
            record = request.scalar_one_or_none()

            if record is None:
                logger.warning("Объект с ID {} не найден".format(data_id))
                return False
            
            await session.delete(record)
            await session.flush()

            return True

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


    @classmethod
    @connection(commit=False)
    async def exists(cls, session: AsyncSession, data_id: str):
        try:
            response = await cls.find_by_id(data_id=data_id)

            if response is None:
                logger.warning("Объект с ID {} не существует".format(data_id))
                return False

            return True
        
        except SQLAlchemyError as e:
            logger.error("Ошибка при проверке наличия объекта с ID {}, ошибка: {}".format(data_id, e))
            raise
