import asyncio

from contextlib import asynccontextmanager
from functools import wraps
from logging import Logger
from socket import gaierror
from sqlalchemy import update, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncGenerator
from uuid import UUID

from core.config import settings as st
from models.base import Base
from models.tasks import Task
from schemas.tasks import TaskS


engine = create_async_engine(
    st.dsn_postgres,
    pool_pre_ping=True,
    pool_recycle=st.pool_recycle,
    pool_size=st.pool_size,
    max_overflow=st.max_overflow,
    future=True
)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


class DBError:
    pass


def connect_saver(func):
    @wraps(func)
    async def wrapper(self: 'DB', *args, **kwargs):
        attempts = 0
        while True:
            try:
                result = await func(self, *args, **kwargs)
                return result
            except (OperationalError, gaierror) as e:
                attempts += 1
                self.logger.error(
                    'Failed to reconnect to PostgreSQL (attempt = %s). '
                    'Error_type = %s, error_msg=%s',
                    attempts, type(e), str(e)
                )

                time_sleep = st.start_sleep_time * (st.factor ** attempts)
                if time_sleep > st.border_sleep_time:
                    time_sleep = st.border_sleep_time
                await asyncio.sleep(time_sleep)
            except Exception as e:
                self.logger.error(
                    'Failed to reconnect to PostgreSQL (attempt = %s). '
                    'Error_type = %s, error_msg=%s',
                    attempts, type(e), str(e)
                )
                return DBError()
    return wrapper


class DB:
    def __init__(self, db_table: Base, logger: Logger):
        self.db_table = db_table
        self.logger = logger

    @connect_saver
    async def get(self, task_id: UUID) -> TaskS:
        async with get_session() as session:
            query = select(Task).where(Task.uuid == task_id)
            result = await session.execute(query)
            item = result.scalars().first()
            if not item:
                return None
        return TaskS.model_validate(item, from_attributes=True)

    @connect_saver
    async def update(self, task_id: UUID, update_fields: dict):
        async with get_session() as session:
            stmt = update(
                    Task
                ).where(
                    Task.uuid == task_id
                ).values(
                    **update_fields
                )
            await session.execute(stmt)
            await session.commit()
            return True
