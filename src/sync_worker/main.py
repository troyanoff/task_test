import argparse
import logging
import pika
import signal
import threading
import time

from datetime import datetime
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from uuid import UUID

from core.config import settings as st
from models.tasks import Task, TaskStatus
from schemas.tasks import TaskS
from sync_tasks import task_list


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging.getLogger('pika').setLevel(logging.WARNING)


stop_event = threading.Event()

engine = create_engine(st.dsn_postgres_sync)


class DB:

    def get(self, task_id: UUID):
        with Session(engine) as session:
            stmt = select(Task).where(Task.uuid == task_id)
            task = session.scalars(stmt).one()
        return TaskS.model_validate(task, from_attributes=True)

    def update(self, task_id: UUID, update_fields: dict):
        with Session(engine) as session:
            stmt = update(Task).where(Task.uuid == task_id).values(
                **update_fields)
            session.execute(stmt)
            session.commit()


def process_message(
    channel: BlockingChannel,
    method: Basic.Deliver,
    body: bytes
):
    if stop_event.is_set():
        return
    db = DB()
    try:
        task = TaskS.model_validate_json(body.decode())
        db_task = db.get(task_id=task.uuid)
        if db_task.status == TaskStatus.CANCELLED:
            logger.info(f'{task.uuid=} was CANCELLED')
            return

        logger.info(f'Processing: {task.uuid=}')

        db.update(
            task_id=task.uuid,
            update_fields=TaskS(
                status=TaskStatus.IN_PROGRESS,
                started_at=datetime.now()
            ).model_dump(exclude_unset=True)
        )

        result = task_list[task.name](**task.params)

        channel.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f'Completed: {task.uuid=}, {result=}')
        db.update(
            task_id=task.uuid,
            update_fields=TaskS(
                status=TaskStatus.COMPLETED,
                completed_at=datetime.now(),
                result=result
            ).model_dump(exclude_unset=True)
        )

    except Exception as e:
        logger.error(f'Error {e}')
        db.update(
            task_id=task.uuid,
            update_fields=TaskS(
                status=TaskStatus.FAILED,
                exc_info=str(e)
            ).model_dump(exclude_unset=True)
        )


def worker(queue_name: str):
    logger.info('Start worker')
    connection = None
    try:
        connection = pika.BlockingConnection(pika.URLParameters(st.dsn_rebbit))
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        while not stop_event.is_set():
            method_frame, _, body = channel.basic_get(
                queue=queue_name, auto_ack=False)
            if method_frame:
                process_message(channel, method_frame, body)
            else:
                time.sleep(0.2)
    except Exception as e:
        logger.info(f'Worker error: {e}')
    finally:
        if connection and connection.is_open:
            connection.close()
        logger.info('Worker stopped')


def signal_handler(sig, frame):
    stop_event.set()


def parse_args():
    parser = argparse.ArgumentParser(
        description='RabbitMQ Sync Worker with Thread Pool')
    parser.add_argument(
        '--queue',
        required=True,
        help='RabbitMQ queue name to consume from'
    )
    parser.add_argument(
        '--threads',
        type=int,
        default=4,
        help='Threads count (default: 4)'
    )
    return parser.parse_args()


def main():
    args = parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    logger.info(f'Created {args.threads} workers')
    threads = []
    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=[args.queue])
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
