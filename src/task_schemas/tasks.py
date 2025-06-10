from datetime import datetime
from uuid import UUID

from models.tasks import TaskPriority, TaskStatus
from schemas.base import MyBaseModel


class TaskS(MyBaseModel):
    uuid: UUID = None
    name: str = None
    description: str | None = None
    priority: TaskPriority = None
    params: dict = None
    created_at: datetime = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    status: TaskStatus = None
    exc_info: str | None = None
    result: dict | None = None
