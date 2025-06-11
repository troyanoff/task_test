import logging
import time

from datetime import datetime
from functools import wraps
from pika import BlockingConnection, URLParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPError
from pika.spec import Basic
from socket import gaierror
from threading import Event

from core.config import settings as st
from models.tasks import TaskStatus
from schemas.tasks import TaskS
from sync_tasks import task_list
from db_operations import DB


def connect_saver(func):
    @wraps(func)
    def wrapper(self: 'Worker', *args, **kwargs):
        attempts = 0
        while not self.stop_event.is_set():
            try:
                self.create_connection()
                result = func(self, *args, **kwargs)
                return result
            except (AMQPError, gaierror) as e:
                attempts += 1
                self.logger.error(
                    'Failed to connect to RabbitMQ (attempt = %s) '
                    'error_type=%s, error_msg=%s',
                    attempts, type(e), str(e)
                )
                time_sleep = st.start_sleep_time * (st.factor ** attempts)
                if time_sleep > st.border_sleep_time:
                    time_sleep = st.border_sleep_time
                time.sleep(time_sleep)
            except Exception as e:
                self.logger.error(
                    'type=%s, str=%s',
                    type(e), str(e)
                )

        self.stop()
    return wrapper


class Worker:
    def __init__(
        self,
        worker_name: str,
        queue_name: str,
        stop_event: Event,
        logger: logging.Logger
    ):
        self.worker_name = worker_name
        self.queue_name = queue_name
        self.stop_event = stop_event
        self.logger = logger
        self.db = DB(stop_event, logger)
        self.connection: BlockingConnection = None
        self.channel: BlockingChannel = None

    def stop(self):
        try:
            if self.channel and self.channel.is_open:
                self.channel.close()
            if self.connection and self.connection.is_open:
                self.connection.close()
        except Exception:
            self.logger.error('Unexpected error', exc_info=True)

    def create_connection(self):
        params = URLParameters(url=st.dsn_rebbit)
        params.heartbeat = st.heartbeat
        params.blocked_connection_timeout = st.blocked_connection_timeout
        params.retry_delay = st.retry_delay
        params.socket_timeout = st.socket_timeout

        self.connection = BlockingConnection(params)
        self.logger.info('Successfully connected to RabbitMQ')

    def message_handler(
        self,
        channel: BlockingChannel,
        method: Basic.Deliver,
        _,
        body: bytes
    ):
        try:
            task = TaskS.model_validate_json(body.decode())

            db_task = self.db.get(task_id=task.uuid)
            if not db_task:
                self.logger.error(
                    'Failed to get task %s from database', task.uuid
                )
                channel.basic_ack(delivery_tag=method.delivery_tag)
                return
            if db_task.status == TaskStatus.CANCELLED:
                self.logger.info('task.uuid=%s was CANCELLED', task.uuid)
                channel.basic_ack(delivery_tag=method.delivery_tag)
                return

            self.logger.info('Processing: task.uuid=%s', task.uuid)

            success_update = self.db.update(
                task_id=task.uuid,
                update_fields=TaskS(
                    status=TaskStatus.IN_PROGRESS,
                    started_at=datetime.now()
                ).model_dump(exclude_unset=True)
            )
            if not success_update:
                self.logger.error(
                    'Failed to update task %s status to %s',
                    task.uuid, 'IN_PROGRESS'
                )
                return

            result = task_list[task.name](**task.params)

            channel.basic_ack(delivery_tag=method.delivery_tag)
            self.logger.info(
                'Completed: task.uuid=%s, result=%s',
                task.uuid, result
            )

            success_update = self.db.update(
                task_id=task.uuid,
                update_fields=TaskS(
                    status=TaskStatus.COMPLETED,
                    completed_at=datetime.now(),
                    result=result
                ).model_dump(exclude_unset=True)
            )
            if not success_update:
                self.logger.error(
                    'Failed to update task %s status to %s',
                    task.uuid, 'COMPLETED'
                )

        except Exception as e:
            self.logger.error(
                'Error processing message: task.uuid=%s',
                task.uuid,
                exc_info=True
            )
            success_update = self.db.update(
                task_id=task.uuid,
                update_fields=TaskS(
                    status=TaskStatus.FAILED,
                    exc_info=str(e)
                ).model_dump(exclude_unset=True)
            )
            channel.basic_ack(delivery_tag=method.delivery_tag)
            if not success_update:
                self.logger.error(
                    'Failed to update task %s status to %s',
                    task.uuid, 'FAILED'
                )

    @connect_saver
    def start(self):
        self.logger.info(
            'Starting worker_name=%s for queue=%s',
            self.worker_name, self.queue_name
        )
        channel = self.connection.channel()
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.message_handler,
            auto_ack=False
        )
        self.channel = channel
        try:
            channel.start_consuming()
        except Exception as e:
            self.logger.error(
                '\nUnexpected error:\ntype=%s,\nmsg=%s',
                type(e), str(e)
            )
