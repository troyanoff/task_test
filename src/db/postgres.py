from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
from typing import AsyncGenerator

from core.config import settings as st


engine = create_async_engine(st.dsn_postgres, future=True)
async_session = sessionmaker(
    engine, class_=_AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[_AsyncSession, None]:
    async with async_session() as session:
        yield session
