from celery import Celery, Task
from kombu import Queue, Exchange

from core.config import settings as st
from core.celery_task import CustomTask


celery_app = Celery('worker')
celery_app.Task = CustomTask
celery_app.conf.update(
    broker_url=st.dsn_celery_broker,
    # result_backend=st.dsn_celery_backend,

    result_extended=True,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,

    task_acks_late=True,
    task_queues=[
        Queue(
            'fast_tasks',
            Exchange('fast_tasks'),
            routing_key='fast_tasks',
            queue_arguments={'x-max-priority': 10}
        ),
        Queue(
            'normal_tasks',
            Exchange('normal_tasks'),
            routing_key='normal_tasks',
            queue_arguments={'x-max-priority': 10}
        ),
        Queue(
            'slow_tasks',
            Exchange('slow_tasks'),
            routing_key='slow_tasks',
            queue_arguments={'x-max-priority': 10}
        ),
    ],
    # task_routes={
    #     'app.tasks.fast_tasks.*': {
    #         'queue': 'fast_tasks',
    #         'routing_key': 'fast_tasks',
    #     },
    #     'app.tasks.normal_tasks.*': {
    #         'queue': 'normal_tasks',
    #         'routing_key': 'normal_tasks',
    #     },
    #     'app.tasks.slow_tasks.*': {
    #         'queue': 'slow_tasks',
    #         'routing_key': 'slow_tasks',
    #     },
    # },

    task_default_queue='normal_tasks',

    worker_pool='gevent',
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
    broker_transport_options={'prefetch_count': 1},
)

celery_app.autodiscover_tasks(
    [
        'tasks.fast_tasks',
        'tasks.normal_tasks'
    ],
    force=True
)

exist_tasks: dict[str, Task] = celery_app.tasks
