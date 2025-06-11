from aio_pika import Channel, Message, DeliveryMode
from fastapi import Depends
from functools import lru_cache

from db.rebbit import get_rabbit_channel


class QueueService:
    def __init__(self, channel: Channel):
        self.channel = channel

    async def send_to_queue(
        self,
        queue_name: str,
        message: str,
        priority: int = 5
    ):
        await self.channel.default_exchange.publish(
            Message(
                body=message.encode(),
                delivery_mode=DeliveryMode.PERSISTENT,
                priority=priority
            ),
            routing_key=queue_name
        )


@lru_cache()
def get_queue_service(
    channel: Channel = Depends(get_rabbit_channel),
) -> QueueService:
    return QueueService(
        channel=channel,
    )
