from fastapi import Depends
from functools import lru_cache
from http import HTTPStatus
from sqlalchemy import select, update, func, Select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from db.postgres import get_session
from models.tasks import Task
from schemas.tasks import TaskToDBS, TaskS, TaskListS
from schemas.exceptions import ExcBaseS


class TaskService:
    db_table = Task

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _check_kwargs(self, **kwargs: dict):
        """Check kwargs exist."""
        if not kwargs:
            return kwargs
        result = {}
        for k, v in kwargs.items():
            if v is not None:
                result[k] = v
        return result

    async def _add_where_operator(self, query: Select, **kwargs) -> Select:
        kwargs_exist: dict = await self._check_kwargs(**kwargs)
        if kwargs_exist:
            where_clauses = [
                getattr(self.db_table, key) == value
                for (key, value) in kwargs_exist.items()
            ]
            query = query.where(and_(*where_clauses))
        return query

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

    async def get(self, item_id: UUID) -> TaskS | None:
        query = select(self.db_table).where(self.db_table.uuid == item_id)
        result = await self.session.execute(
            query
        )
        item = result.scalars().first()
        if not item:
            return ExcBaseS(
                msg='task not found',
                code=HTTPStatus.NOT_FOUND
            )
        return TaskS.model_validate(item, from_attributes=True)

    async def update(self, task_id: UUID, update_fields: dict):
        stmt = update(
                self.db_table
            ).where(
                self.db_table.uuid == task_id
            ).values(
                **update_fields
            )
        result = await self.session.execute(stmt)

        if result.rowcount == 0:
            await self.session.rollback()
            return ExcBaseS(
                msg='task not found',
                code=HTTPStatus.NOT_FOUND
            )
        await self.session.commit()

    async def get_list(
        self,
        limit: int,
        offset: int,
        **kwargs
    ) -> TaskListS:
        query = await self._add_where_operator(
            select(self.db_table),
            **kwargs
        )
        query = query.order_by(
            self.db_table.created_at.desc()).limit(limit).offset(offset)

        query_total_count = await self._add_where_operator(
            select(func.count(self.db_table.uuid)),
            **kwargs
        )

        db_items = await self.session.execute(query)
        total_count = await self.session.execute(query_total_count)
        total_count = total_count.scalars().first()
        db_items = db_items.scalars().unique()
        items = [TaskS.model_validate(item, from_attributes=True)
                 for item in db_items]
        list_schema = TaskListS(
            items=items,
            total_count=total_count)

        return list_schema


@lru_cache()
def get_task_service(
    session: AsyncSession = Depends(get_session),
) -> TaskService:
    return TaskService(
        session=session,
    )
