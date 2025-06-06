from celery.result import AsyncResult
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4

from core.celery_config import celery_app
from core.config import settings as st
from schemas.exceptions import ExcBaseS
from schemas.tasks import BaseTaskS, TaskCreateS, TaskToDBS, TaskS
from services.tasks import get_task_service, TaskService
from tasks.fast_tasks.tasks import fast_default


router = APIRouter()


@router.post(
    '/',
    response_model=BaseTaskS,
    response_model_by_alias=False,
    summary='Create',
    description='Create new task',
)
async def create(
    body: TaskCreateS,
    service: TaskService = Depends(get_task_service),
) -> BaseTaskS:
    """Create new task."""
    item = TaskToDBS.model_validate(body)
    db_item = service.create(item)

    if isinstance(db_item, ExcBaseS):
        raise HTTPException(
            status_code=db_item.code,
            detail=db_item.msg,
        )

    fast_default.apply_async(
        args=[body.name],
        task_id=item.uuid,
        priority=item.priority_code,
    )

    return BaseTaskS(uuid=item.uuid)


@router.get(
    '/{task_id}',
    # response_model=BaseTaskS,
    response_model_by_alias=False,
    summary='Task info',
    description='Show task info',
)
async def task_info(
    task_id: str
):
    task_result = AsyncResult(task_id)
    print(task_result)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None,
    }
