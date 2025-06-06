from fastapi import Depends
from functools import lru_cache
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models.tasks import Task
from schemas.tasks import TaskToDBS, TaskS
from schemas.exceptions import ExcBaseS


class TaskService:
    db_table = Task

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, item: TaskToDBS) -> TaskS | ExcBaseS:
        try:
            db_item = self.db_table(**item.model_dump())
            self.session.add(db_item)
            await self.session.commit()
            return TaskS.model_validate(db_item, from_attributes=True)
        except IntegrityError:
            return ExcBaseS(
                msg='bad data in body',
                code=HTTPStatus.BAD_REQUEST
            )


@lru_cache()
def get_task_service(
    session: AsyncSession = Depends(get_session),
) -> TaskService:
    return TaskService(
        session=session,
    )
