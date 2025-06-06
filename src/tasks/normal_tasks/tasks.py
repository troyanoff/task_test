import asyncio

from core.celery_config import celery_app


@celery_app.task(queue='normal_tasks')
async def normal_default():
    await asyncio.sleep(1)
    return 'normal_default'
