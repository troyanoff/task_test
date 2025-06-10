from datetime import datetime
from pydantic import Field, computed_field, field_validator
from uuid import UUID, uuid4

from core.config import settings as st
from models.tasks import TaskPriority, TaskStatus
from schemas.base import MyBaseModel


class BaseTaskS(MyBaseModel):
    uuid: UUID


class TaskStatusS(MyBaseModel):
    status: TaskStatus


class TaskCreateS(MyBaseModel):
    name: str
    params: dict
    priority: TaskPriority = TaskPriority.MEDIUM

    @field_validator('name', mode='after')
    @classmethod
    def check_name(cls, value: str) -> str:
        if not st.task_name_queue_match.get(value):
            raise ValueError('task name not found')
        return value


class TaskToDBS(TaskCreateS):
    uuid: UUID = Field(default_factory=lambda: uuid4())

    @property
    def priority_code(self) -> int:
        metch = {
            TaskPriority.HIGH: 10,
            TaskPriority.MEDIUM: 5,
            TaskPriority.LOW: 1
        }
        return metch[self.priority]

    @computed_field
    @property
    def description(self) -> str:
        return st.task_description[self.name]


class TaskS(BaseTaskS):
    name: str
    description: str | None
    priority: TaskPriority
    params: dict
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    status: TaskStatus
    exc_info: str | None
    result: dict | None


class TaskListS(MyBaseModel):
    items: list[TaskS]
    total_count: int
