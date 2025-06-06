from dotenv import load_dotenv
from logging import config as logging_config
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings

from core.logger import LOGGING


load_dotenv()


# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = Field('project name', alias='PROJECT_NAME')

    db_prefix: str = Field('postgresql+asyncpg', alias='DB_PREFIX')
    db_prefix_celery: str = Field('db+postgresql', alias='DB_PREFIX_CELERY')
    db_user: str = Field('postgres_user', alias='POSTGRES_USER')
    db_password: str = Field('postgres_password', alias='POSTGRES_PASSWORD')
    db_host: str = Field('127.0.0.1', alias='POSTGRES_HOST')
    db_port: int = Field(5432, alias='POSTGRES_PORT')
    db_name: str = Field('postgres_db_name', alias='POSTGRES_DB')

    broker_prefix: str = Field('amqp', alias='BROKER_PREFIX')
    broker_user: str = Field('guest', alias='BROKER_USER')
    broker_password: str = Field('guest', alias='BROKER_PASSWORD')
    broker_host: str = Field('rabbitmq', alias='BROKER_HOST')
    broker_port: int = Field(5672, alias='BROKER_PORT')

    @computed_field
    @property
    def dsn_postgres(self) -> str:
        return (
            f'{self.db_prefix}://'
            f'{self.db_user}:{self.db_password}@{self.db_host}:'
            f'{self.db_port}/{self.db_name}'
        )

    @computed_field
    @property
    def dsn_celery_backend(self) -> str:
        return (
            f'{self.db_prefix_celery}://'
            f'{self.db_user}:{self.db_password}@{self.db_host}:'
            f'{self.db_port}/{self.db_name}'
        )

    @computed_field
    @property
    def dsn_celery_broker(self) -> str:
        return (
            f'{self.broker_prefix}://'
            f'{self.broker_user}:{self.broker_password}@'
            f'{self.broker_host}:{self.broker_port}//'
        )


settings = Settings()
