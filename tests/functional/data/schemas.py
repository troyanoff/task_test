from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from uuid import UUID


class CreateTaskResponse(BaseModel):
    uuid: UUID

    model_config = {
        'extra': 'forbid'
    }


class TaskPriority(str, Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


class TaskStatus(str, Enum):
    NEW = 'NEW'
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    CANCELLED = 'CANCELLED'


class StatusTaskResponse(BaseModel):
    status: TaskStatus

    model_config = {
        'extra': 'forbid'
    }


class InfoTaskSchema(BaseModel):
    uuid: UUID
    name: str
    description: str
    params: dict
    priority: TaskPriority
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    status: TaskStatus
    exc_info: str | None
    result: dict | None

    model_config = {
        'extra': 'forbid'
    }


class ListTaskSchema(BaseModel):
    items: list[InfoTaskSchema]
    total_count: int
