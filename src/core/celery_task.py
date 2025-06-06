from celery import Task

from db.postgres import get_session_celery
from models.tasks import Task as TaskDB


class CustomTask(Task):
    def update_state(self, task_id=None, state=None, meta=None):
        super().update_state(task_id=task_id, state=state, meta=meta)
        self._update_task_in_db(task_id or self.request.id, state, meta)

    def _update_task_in_db(self, task_id, state, meta):
        with get_session_celery() as session:
            task = session.query(TaskDB).filter(TaskDB.uuid == task_id).first()
            if not task:
                task = TaskDB(task_id=task_id)
                session.add(task)

            task.status = state
            if meta:
                if 'progress' in meta:
                    task.progress = meta['progress']
                task.metadata = meta
            session.commit()
