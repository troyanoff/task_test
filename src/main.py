import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
# from contextlib import asynccontextmanager

from api.v1 import (
    tasks
)
from core.config import settings as st

print(st)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     redis.redis = Redis(host=st.redis_host, port=st.redis_port)
#     await FastAPILimiter.init(redis.redis)
#     # await create_database()
#     # Раскомментить для локального запуска.
#     # os.system('alembic revision --autogenerate -m 'Initial tables'')
#     # os.system('alembic upgrade head')
#     # os.system('python3 create_superuser.py')
#     yield
#     await redis.redis.close()


app = FastAPI(
    title=st.project_name,
    description='Управление задачами.',
    docs_url='/api/doc',
    openapi_url='/api/doc.json',
    default_response_class=ORJSONResponse,
    version='1.0.0',
)


app.include_router(
    tasks.router,
    prefix='/api/v1/tasks',
    tags=['Tasks']
)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=7557,
        reload=True,
        workers=4
    )
