import asyncio


async def send_email(*args, **kwargs):
    await asyncio.sleep(10)
    if 'failed' in kwargs.keys():
        2 / 0
    return {'result': 'Done'}
