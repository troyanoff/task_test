from dotenv import load_dotenv
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    project_name: str = Field('project name', alias='PROJECT_NAME')
    service_host: str = Field('localhost', alias='SERVICE_HOST')
    service_port: str = Field('', alias='SERVICE_PORT')

    storage: dict = {}

    default_workers: int = 5
    default_task_compled_timeout: int = 5

    canceled_task_flags: tuple = (
        'cancel_fast_io', 'cancel_normal_io', 'cancel_slow_io',
        'cancel_fast_cpu', 'cancel_normal_cpu', 'cancel_slow_cpu',
    )

    @computed_field
    @property
    def service_url(self) -> str:
        return f'http://{self.service_host}:{self.service_port}/'


settings = Settings()
