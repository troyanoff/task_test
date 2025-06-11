import time

from functools import wraps
from logging import Logger
from sqlalchemy import create_engine, select, update
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from threading import Event
from uuid import UUID

from core.config import settings as st
from models.tasks import Task
from schemas.tasks import TaskS


def create_db_engine():
    return create_engine(
        st.dsn_postgres_sync,
        pool_pre_ping=True,
        pool_recycle=st.pool_recycle,
        pool_size=st.pool_size,
        max_overflow=st.max_overflow,
        future=True
    )


def connect_saver(func):
    @wraps(func)
    def wrapper(self: 'DB', *args, **kwargs):
        attempts = 0
        while not self.stop_event.is_set():
            try:
                result = func(self, *args, **kwargs)
                return result
            except OperationalError:
                reconnect = self._reconnect()
                if reconnect:
                    continue
                attempts += 1
                self.logger.error(
                    'Failed to reconnect to PostgreSQL (attempt %s)', attempts,
                    exc_info=True
                )

                time_sleep = st.start_sleep_time * (st.factor ** attempts)
                if time_sleep > st.border_sleep_time:
                    time_sleep = st.border_sleep_time
                time.sleep(time_sleep)
    return wrapper


class DB:
    def __init__(self, stop_event: Event, logger: Logger):
        self.stop_event = stop_event
        self.logger = logger
        self.engine = create_db_engine()

    def _reconnect(self) -> bool:
        """Trying to reconnect to database."""
        try:
            self.engine.dispose()
            self.engine = create_db_engine()

            # check connect
            with Session(self.engine) as session:
                session.execute(select(1))

            self.logger.info('Successfully reconnected to PostgreSQL')
            return True
        except OperationalError:
            return False

    @connect_saver
    def get(self, task_id: UUID) -> TaskS:
        """Get item from db."""
        with Session(self.engine) as session:
            stmt = select(Task).where(Task.uuid == task_id)
            task = session.scalars(stmt).first()
            if not task:
                return None
            return TaskS.model_validate(task, from_attributes=True)

    @connect_saver
    def update(self, task_id: UUID, update_fields: dict) -> bool:
        """Update db item."""
        with Session(self.engine) as session:
            stmt = update(Task).where(Task.uuid == task_id).values(
                **update_fields)
            session.execute(stmt)
            session.commit()
            return True
