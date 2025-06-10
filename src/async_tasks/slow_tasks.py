import asyncio


async def send_files(*args, **kwargs):
    await asyncio.sleep(30)
    return {'result': 'Done'}
