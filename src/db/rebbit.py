import aio_pika

from typing import AsyncGenerator

from core.config import settings as st


async def get_rabbit_channel() -> AsyncGenerator[aio_pika.Channel, None]:
    connection = await aio_pika.connect_robust(st.dsn_rebbit)
    async with connection.channel() as channel:
        yield channel


async def setup_queues():
    connection = await aio_pika.connect_robust(st.dsn_rebbit)
    channel = await connection.channel()

    for q in st.queues_config:
        await channel.declare_queue(
            q['name'],
            durable=True,
            arguments={'x-max-priority': q['priority']}
        )

    await connection.close()
