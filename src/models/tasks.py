from enum import Enum
from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from models.base import Base


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


class Task(Base):
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    params: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    priority: Mapped[TaskPriority] = mapped_column(
        default=TaskPriority.MEDIUM, index=True
    )
    started_at: Mapped[datetime | None] = mapped_column(nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        default=TaskStatus.NEW, index=True
    )
    exc_info: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    result: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    def __repr__(self) -> str:
        return f'<Task {self.uuid}>'
