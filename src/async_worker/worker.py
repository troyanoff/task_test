import asyncio

from aio_pika import IncomingMessage, connect_robust
from aio_pika.exceptions import AMQPError
from datetime import datetime
from functools import wraps
from logging import Logger
from socket import gaierror
from typing import Any

from core.config import settings as st
from db_operations import DBError, DB
from models.tasks import TaskStatus
from schemas.tasks import TaskS


def connect_saver(func):
    @wraps(func)
    async def wrapper(self: 'AsyncWorker', *args, **kwargs):
        attempts = 0
        while True:
            try:
                await self.create_connection()
                result = await func(self, *args, **kwargs)
                return result
            except (AMQPError, gaierror, RuntimeError) as e:
                attempts += 1
                self.logger.error(
                    'Failed to connect to RabbitMQ (attempt = %s) '
                    'error_type=%s, error_msg=%s',
                    attempts, type(e), str(e)
                )
                time_sleep = st.start_sleep_time * (st.factor ** attempts)
                if time_sleep > st.border_sleep_time:
                    time_sleep = st.border_sleep_time
                await asyncio.sleep(time_sleep)
            except Exception as e:
                self.logger.error(
                    'type=%s, str=%s',
                    type(e), str(e)
                )
                self.stop()
                return
    return wrapper


class AsyncWorker:
    def __init__(
        self,
        logger: Logger,
        worker_name: str,
        db: DB,
        rabbitmq_url: str,
        queue_name: str,
        task_name_match: dict,
        max_concurrent_tasks: int
    ):
        self.logger = logger
        self.worker_name = worker_name
        self.db = db
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.max_concurrent_tasks = max_concurrent_tasks
        self.task_name_match = task_name_match
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)
        self.connection = None
        self.channel = None
        self.queue = None
        self.run_worker = True

    async def bad_db_response(self, result: Any, message: IncomingMessage):
        if isinstance(result, DBError):
            self.logger.error('Error db connection')
            self.run_worker = False
            await message.nack()
            return True
        return False

    async def create_connection(self):
        self.connection = await connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=self.max_concurrent_tasks)

        self.queue = await self.channel.declare_queue(
            self.queue_name,
            durable=True,
            arguments={
                'x-max-priority': 10
            }
        )

    async def process_task(self, message: IncomingMessage):
        async with self.semaphore:
            async with message.process():
                task = TaskS.model_validate_json(message.body.decode())
                db_task = await self.db.get(
                    task_id=task.uuid)

                if await self.bad_db_response(db_task, message):
                    return

                if db_task.status == TaskStatus.CANCELLED:
                    self.logger.info(
                        'task.uuid=%s was CANCELLED',
                        task.uuid
                    )
                    return

                self.logger.info(
                    'Processing task with uuid=%s',
                    task.uuid
                )

                result = await self.db.update(
                    task.uuid,
                    TaskS(
                        status=TaskStatus.IN_PROGRESS,
                        started_at=datetime.now()
                    ).model_dump(exclude_unset=True)
                )

                if await self.bad_db_response(result, message):
                    return

                try:
                    result_task = await self.execute_task(task)
                except Exception as e:
                    result = await self.db.update(
                        task.uuid,
                        TaskS(
                            status=TaskStatus.FAILED,
                            exc_info=str(e)
                        ).model_dump(exclude_unset=True)
                    )
                    if await self.bad_db_response(result, message):
                        return
                    self.logger.error(
                        'Error processing task: '
                        'uuid=%s, error_type=%s, error_mag=%s',
                        task.uuid, type(e), str(e)
                    )
                    return

                result = await self.db.update(
                    task.uuid,
                    TaskS(
                        status=TaskStatus.COMPLETED,
                        completed_at=datetime.now(),
                        result=result_task
                    ).model_dump(exclude_unset=True)
                )

                if await self.bad_db_response(result, message):
                    return

                self.logger.info(
                    'Task completed. uuid=%s, result=%s',
                    task.uuid, result_task
                )

    async def execute_task(self, task: TaskS):
        result = await self.task_name_match[task.name](
            **task.params)
        return result

    @connect_saver
    async def start(self):
        self.logger.info(
            'Worker started. Queue: <%s>. '
            'Max concurrent tasks: %s',
            self.queue_name, self.max_concurrent_tasks
        )
        await self.queue.consume(self.process_task)

    async def stop(self):
        if self.connection:
            await self.connection.close()
