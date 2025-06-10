import argparse
import asyncio
import logging

from aio_pika import connect, IncomingMessage
from contextlib import asynccontextmanager
from datetime import datetime
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from uuid import UUID

from async_tasks import task_list
from core.config import settings as st
from models.base import Base
from models.tasks import Task, TaskStatus
from db.postgres import async_session
from schemas.tasks import TaskS


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


class DBOperations:
    db_table = Task

    def __init__(self, db_table: Base):
        self.db_table = db_table

    async def get_task(self, task_id: UUID) -> TaskS:
        async with get_session() as session:
            query = select(Task).where(Task.uuid == task_id)
            result = await session.execute(query)
            item = result.scalars().first()
        return TaskS.model_validate(item, from_attributes=True)

    async def update_task_info(self, task_id: UUID, update_fields: dict):
        async with get_session() as session:
            stmt = update(
                    Task
                ).where(
                    Task.uuid == task_id
                ).values(
                    **update_fields
                )
            result = await session.execute(stmt)

            if result.rowcount == 0:
                await session.rollback()
                logger.warning(f'Task with uuid={task_id} not found')
            await session.commit()


class AsyncWorker:
    def __init__(
        self,
        db_operations: DBOperations,
        rabbitmq_url: str,
        queue_name: str,
        task_name_match: dict,
        max_concurrent_tasks: int = 5,
    ):
        self.db_operations = db_operations
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.max_concurrent_tasks = max_concurrent_tasks
        self.task_name_match = task_name_match
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)
        self.connection = None
        self.channel = None
        self.queue = None

    async def process_task(self, message: IncomingMessage):
        async with self.semaphore:
            try:
                async with message.process():
                    task = TaskS.model_validate_json(message.body.decode())
                    db_task = await self.db_operations.get_task(
                        task_id=task.uuid)
                    if db_task.status == TaskStatus.CANCELLED:
                        logger.info(f'{task.uuid=} was CANCELLED')
                        return

                    logger.info(
                        f'Processing task from queue <{self.queue_name}>: '
                        f'{task.uuid=}')

                    await self.db_operations.update_task_info(
                        task.uuid,
                        TaskS(
                            status=TaskStatus.IN_PROGRESS,
                            started_at=datetime.now()
                        ).model_dump(exclude_unset=True)
                    )

                    result = await self.execute_task(task)

                    await self.db_operations.update_task_info(
                        task.uuid,
                        TaskS(
                            status=TaskStatus.COMPLETED,
                            completed_at=datetime.now(),
                            result=result
                        ).model_dump(exclude_unset=True)
                    )

                    logger.info(f'Task completed. Result: {result}')
            except Exception as e:
                await self.db_operations.update_task_info(
                    task.uuid,
                    TaskS(
                        status=TaskStatus.FAILED,
                        exc_info=str(e)
                    ).model_dump(exclude_unset=True)
                )
                logger.error(f'Error processing task: {e}')

    async def execute_task(self, task: TaskS):
        result = await self.task_name_match[task.name](
            task.params)
        return result

    async def start(self):
        self.connection = await connect(self.rabbitmq_url)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=self.max_concurrent_tasks)

        self.queue = await self.channel.declare_queue(
            self.queue_name,
            durable=True,
            arguments={
                'x-max-priority': 10
            }
        )

        logger.info(
            f'Worker started. Queue: <{self.queue_name}>. '
            f'Max concurrent tasks: {self.max_concurrent_tasks}'
        )
        await self.queue.consume(self.process_task)

    async def stop(self):
        if self.connection:
            await self.connection.close()


def parse_args():
    parser = argparse.ArgumentParser(description='Async RabbitMQ worker')
    parser.add_argument(
        '-q', '--queue',
        required=True,
        help='RabbitMQ queue name to consume from'
    )
    parser.add_argument(
        '--rabbitmq-url',
        default=st.dsn_rebbit,
        help=f'RabbitMQ connection URL (default: {st.dsn_rebbit})'
    )
    parser.add_argument(
        '--max-tasks',
        type=int,
        default=5,
        help='Max concurrent tasks (default: 5)'
    )
    return parser.parse_args()


async def main():
    args = parse_args()

    worker = AsyncWorker(
        db_operations=DBOperations(db_table=Task),
        rabbitmq_url=args.rabbitmq_url,
        queue_name=args.queue,
        max_concurrent_tasks=args.max_tasks,
        task_name_match=task_list
    )

    try:
        await worker.start()
        await asyncio.Future()
    except KeyboardInterrupt:
        logger.info('Worker stopped by user')
    finally:
        await worker.stop()


if __name__ == '__main__':
    asyncio.run(main())
