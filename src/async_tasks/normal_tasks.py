import asyncio


async def send_emails(*args, **kwargs):
    await asyncio.sleep(20)
    return {'result': 'Done'}
