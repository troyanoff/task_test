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

    db_user: str = Field('postgres_user', alias='POSTGRES_USER')
    db_password: str = Field('postgres_password', alias='POSTGRES_PASSWORD')
    db_host: str = Field('127.0.0.1', alias='POSTGRES_HOST')
    db_port: int = Field(5432, alias='POSTGRES_PORT')
    db_name: str = Field('postgres_db_name', alias='POSTGRES_DB')

    rebbit_user: str = Field('guest', alias='BROKER_USER')
    rebbit_password: str = Field('guest', alias='BROKER_PASSWORD')
    rebbit_host: str = Field('rabbitmq', alias='BROKER_HOST')
    rebbit_port: int = Field(5672, alias='BROKER_PORT')

    queues_config: list[dict] = [
        {'name': 'IO_fast', 'priority': 10},
        {'name': 'IO_normal', 'priority': 10},
        {'name': 'IO_slow', 'priority': 10},
        {'name': 'CPU_fast', 'priority': 10},
        {'name': 'CPU_normal', 'priority': 10},
        {'name': 'CPU_slow', 'priority': 10},
    ]

    task_name_queue_match: dict = {
        'send_email': 'IO_fast',
        'send_emails': 'IO_normal',
        'send_files': 'IO_slow',
        'calc_price': 'CPU_fast',
        'calc_prices': 'CPU_normal',
        'calc_report': 'CPU_slow',
    }

    task_description: dict = {
        'send_email': 'Отправка одного письма',
        'send_emails': 'Отправка нескольких писем',
        'send_files': 'Отправка нескольких файлов',
        'calc_price': 'Расчет цены',
        'calc_prices': 'Расчет нескольких цен',
        'calc_report': 'Составление отчета',
    }

    @computed_field
    @property
    def dsn_postgres(self) -> str:
        return (
            f'postgresql+asyncpg://'
            f'{self.db_user}:{self.db_password}@{self.db_host}:'
            f'{self.db_port}/{self.db_name}'
        )

    @computed_field
    @property
    def dsn_postgres_sync(self) -> str:
        return (
            f'postgresql://'
            f'{self.db_user}:{self.db_password}@{self.db_host}:'
            f'{self.db_port}/{self.db_name}'
        )

    @computed_field
    @property
    def dsn_rebbit(self) -> str:
        return (
            f'amqp://'
            f'{self.rebbit_user}:{self.rebbit_password}@'
            f'{self.rebbit_host}:{self.rebbit_port}/{self.project_name}'
        )


settings = Settings()
