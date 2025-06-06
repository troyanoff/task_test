import asyncio
import functools
import os
import time

from contextlib import contextmanager
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker
)
from werkzeug.security import generate_password_hash


load_dotenv()

dbname = os.environ.get('POSTGRES_DB')
user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
host = os.environ.get('POSTGRES_HOST')
port = os.environ.get('POSTGRES_PORT')

dsn = (
    f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}'
)

superuser_login = os.environ.get('SUPERUSER_LOGIN')
superuser_password = os.environ.get('SUPERUSER_PASSWORD')
superuser_uuid = os.environ.get('SUPERUSER_UUID')
superrole_name = os.environ.get('SUPERROLE_NAME')


def duration(func):
    @contextmanager
    def wrapping_logic():
        start_ts = time.time()
        yield
        dur = time.time() - start_ts
        print('{} took {:.2} seconds'.format(func.__name__, dur))

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            with wrapping_logic():
                return func(*args, **kwargs)
        else:
            async def tmp():
                with wrapping_logic():
                    return (await func(*args, **kwargs))
            return tmp()
    return wrapper


@duration
async def create_superuser(
    session: AsyncSession
):
    password_hash = generate_password_hash(superuser_password)
    description = 'default'
    stmt = (
        "INSERT INTO users (uuid, login, password, description, role, "
        "refresh_token) "
        f"VALUES ('{superuser_uuid}', '{superuser_login}', '{password_hash}', "
        f"'{description}', '{superrole_name}', '');"
    )
    await session.execute(text(stmt))
    await session.commit()


async def async_main() -> None:
    engine = create_async_engine(dsn)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        print('creating super user')
        await create_superuser(session)

    await engine.dispose()


asyncio.run(async_main())
