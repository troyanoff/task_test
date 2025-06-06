from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
from typing import AsyncGenerator, Generator

from core.config import settings as st


engine = create_async_engine(st.dsn_postgres, future=True, echo=True)
async_session = sessionmaker(
    engine, class_=_AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[_AsyncSession, None]:
    async with async_session() as session:
        yield session


engine_sync = create_engine(st.dsn_celery_backend, future=True, echo=True)
sunc_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_session_celery() -> Generator[Session, None, None]:
    with sunc_session() as session:
        yield session


# async def create_database() -> None:
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# async def purge_database() -> None:
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
