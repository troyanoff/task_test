import asyncio


async def send_files(*args, **kwargs):
    await asyncio.sleep(5)
    if 'failed' in kwargs.keys():
        2 / 0
    return {'result': 'Done'}
