import argparse
import logging
import signal
import time

from threading import Event, Thread

from worker import Worker


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logging.getLogger('pika').setLevel(logging.CRITICAL)


def parse_args() -> argparse.Namespace:
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
        default=5,
        help='Number of worker threads (default: 5)'
    )
    return parser.parse_args()


def main():
    args = parse_args()

    logger = logging.getLogger(__name__)
    logger.info(
        'Starting %s workers for queue <%s>',
        args.threads, args.queue
    )
    threads: list[Thread] = []

    try:

        stop_event = Event()
        signal.signal(signal.SIGINT, lambda: stop_event.set())
        signal.signal(signal.SIGTERM, lambda: stop_event.set())

        for i in range(args.threads):
            worker_name = f'Worker_{i+1}'
            worker_logger = logging.getLogger(worker_name)
            worker = Worker(
                worker_name=worker_name,
                queue_name=args.queue,
                stop_event=stop_event,
                logger=worker_logger
            )
            t = Thread(
                target=worker.start,
                name=worker_name,
                daemon=True
            )
            t.start()
            threads.append(t)
            time.sleep(0.1)

        for t in threads:
            t.join()
    except Exception:
        logger.error('Main error', exc_info=True)
    finally:
        logger.info('All workers stopped')


if __name__ == '__main__':
    main()
