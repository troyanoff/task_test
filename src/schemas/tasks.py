from datetime import datetime
from pydantic import Field
from uuid import UUID, uuid4

from models.tasks import TaskPriority, TaskStatus
from schemas.base import MyBaseModel


class BaseTaskS(MyBaseModel):
    uuid: UUID


class TaskCreateS(MyBaseModel):
    name: str
    description: str = None
    priority: TaskPriority = TaskPriority.MEDIUM


class TaskToDBS(TaskCreateS):
    uuid: UUID = Field(default_factory=lambda: uuid4())

    @property
    def priority_code(self) -> int:
        metch = {
            TaskPriority.HIGH: 1,
            TaskPriority.MEDIUM: 5,
            TaskPriority.LOW: 10
        }
        return metch[self.priority]


class TaskS(BaseTaskS):
    name: str
    description: str | None
    priority: TaskPriority
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    status: TaskStatus
    exc_info: str | None
    result: dict | None


class TaskListS(MyBaseModel):
    items: list[TaskS]
    total_count: int
