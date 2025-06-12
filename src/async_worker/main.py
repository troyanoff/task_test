import argparse
import asyncio
import logging

from async_tasks import task_list
from core.config import settings as st
from models.tasks import Task
from db_operations import DB
from worker import AsyncWorker


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

    worker_name = f'Worker_{args.queue}'

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(worker_name)

    worker = AsyncWorker(
        logger=logger,
        worker_name=worker_name,
        db=DB(
            db_table=Task,
            logger=logger
        ),
        rabbitmq_url=args.rabbitmq_url,
        queue_name=args.queue,
        max_concurrent_tasks=args.max_tasks,
        task_name_match=task_list
    )

    try:
        await worker.start()
        await asyncio.Future()
    except KeyboardInterrupt:
        logger.info(f'{worker_name} stopped by user')
    finally:
        await worker.stop()


if __name__ == '__main__':
    asyncio.run(main())
