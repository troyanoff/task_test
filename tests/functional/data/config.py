import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    project_name: str = Field('project name', alias='PROJECT_NAME')
    service_host: str = Field('localhost', alias='SERVICE_HOST')
    service_port: str = Field('', alias='SERVICE_PORT')
    tg_id_list: str = os.environ.get('TG_ID_LIST')
    bot_token: str = os.environ.get('TG_BOT_TOKEN')
    error_file: str = 'test_errors.log'

    pstg_user: str = Field('postgres_user', alias='POSTGRES_USER')
    pstg_password: str = Field('postgres_password', alias='POSTGRES_PASSWORD')
    pstg_host: str = Field('127.0.0.1', alias='POSTGRES_HOST')
    pstg_port: int = Field(5432, alias='POSTGRES_PORT')
    pstg_db_name: str = Field('postgres_db_name', alias='POSTGRES_DB')

    superuser_login: str = os.environ.get('SUPERUSER_LOGIN')
    superuser_password: str = os.environ.get('SUPERUSER_PASSWORD')
    superuser_uuid: str = os.environ.get('SUPERUSER_UUID')

    admin_login: str = 'admin'
    admin_password: str = 'admin'
    admin_role_name: str = 'admin'
    admin_uuid: str = ''

    access_token_superuser: str = ''
    refresh_token_superuser: str = ''

    access_token_admin: str = ''
    refresh_token_admin: str = ''

    safe_rate_limit_seconds: int = 1
    default_cache_ttl: int = Field(5, alias='DEFAULT_CACHE_TTL')

    storage: dict = {}

    async def get_tg_id_list(self) -> list:
        result = self.tg_id_list.split(',')
        if result == ['']:
            result = []
        return result

    async def get_service_url(self) -> str:
        return f'http://{self.service_host}:{self.service_port}/'


settings = Settings()
