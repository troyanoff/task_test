from aio_pika import Channel, Message, DeliveryMode
from fastapi import Depends
from functools import lru_cache
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.rebbit import get_rabbit_channel
from models.tasks import Task
from schemas.tasks import TaskToDBS, TaskS
from schemas.exceptions import ExcBaseS


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
