import time

from celery import Task

from core.celery_config import celery_app


@celery_app.task(bind=True, queue='fast_tasks')
def fast_default(self: Task, value: str):
    self.update_state(
        state='IN_PROGRESS',
        meta={
            'meta field from update state method': 'lkl',
            'start_time': time.time().__int__()
        }
    )
    time.sleep(60)
    self.request.custom_data = {
        'initiator': 'user123',
        'priority_level': 'high',
        'source_system': 'CRM'
    }
    return 'fast_task'
