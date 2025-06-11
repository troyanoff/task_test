from fastapi import APIRouter, Depends, HTTPException, status
from http import HTTPStatus

from core.config import settings as st
from models.tasks import TaskStatus, TaskPriority
from schemas.exceptions import ExcBaseS
from schemas.tasks import (
    BaseTaskS, TaskCreateS, TaskToDBS, TaskS, TaskListS, TaskStatusS
)
from services.queues import get_queue_service, QueueService
from services.tasks import get_task_service, TaskService


router = APIRouter()


@router.post(
    '/',
    response_model=BaseTaskS,
    response_model_by_alias=False,
    summary='Create',
    description='Creating new task',
    status_code=status.HTTP_201_CREATED
)
async def create(
    body: TaskCreateS,
    task_service: TaskService = Depends(get_task_service),
    queue_service: QueueService = Depends(get_queue_service),
) -> BaseTaskS:
    item = TaskToDBS.model_validate(body, from_attributes=True)

    db_item = await task_service.create(item)

    if isinstance(db_item, ExcBaseS):
        raise HTTPException(
            status_code=db_item.code,
            detail=db_item.msg,
        )

    await queue_service.send_to_queue(
        queue_name=st.task_name_queue_match[item.name],
        message=item.model_dump_json(),
        priority=item.priority_code
    )

    await task_service.update(
        item.uuid, {'status': TaskStatus.PENDING})

    return BaseTaskS(uuid=item.uuid)


@router.get(
    '/{task_id}',
    response_model=TaskS,
    response_model_by_alias=False,
    summary='Task info',
    description='Show task info',
)
async def task_info(
    task_id: str,
    task_service: TaskService = Depends(get_task_service),
) -> TaskS:
    item = await task_service.get(task_id)
    if isinstance(item, ExcBaseS):
        raise HTTPException(
            status_code=item.code,
            detail=item.msg,
        )
    return item


@router.get(
    '/{task_id}/status',
    response_model=TaskStatusS,
    response_model_by_alias=False,
    summary='Task status',
    description='Show task status',
)
async def task_status(
    task_id: str,
    task_service: TaskService = Depends(get_task_service),
) -> TaskStatusS:
    item = await task_service.get(task_id)
    if isinstance(item, ExcBaseS):
        raise HTTPException(
            status_code=item.code,
            detail=item.msg,
        )
    return TaskStatusS(status=item.status)


@router.delete(
    '/{task_id}',
    summary='Task cancel',
    description='Removing tasks from the queue',
    status_code=status.HTTP_204_NO_CONTENT
)
async def cancel_task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service),
):
    item = await task_service.get(task_id)
    if isinstance(item, ExcBaseS):
        raise HTTPException(
            status_code=item.code,
            detail=item.msg,
        )
    if item.status not in (TaskStatus.NEW, TaskStatus.PENDING):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Task IN_PROGRESS or COMPLETED',
        )

    result = await task_service.update(
        task_id, {'status': TaskStatus.CANCELLED})
    if isinstance(result, ExcBaseS):
        raise HTTPException(
            status_code=result.code,
            detail=result.msg,
        )


@router.get(
    '/',
    response_model=TaskListS,
    response_model_by_alias=False,
    summary='Task list',
    description='Get task list',
)
async def get_all(
    limit: int = 20,
    offset: int = 0,
    status: TaskStatus = None,
    priority: TaskPriority = None,
    task_service: TaskService = Depends(get_task_service),
) -> TaskListS:
    objs = await task_service.get_list(
        limit,
        offset,
        status=status,
        priority=priority,
    )
    return objs
