from functools import lru_cache
from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        env_file_encoding='utf-8'
    )

    app_name: str = 'Purrfect Home API'
    debug: bool = True
    api_v1_prefix: str = '/api/v1/'

    postgres_user: str
    postgres_db: str
    postgres_password: str
    postgres_host: str = 'localhost'
    postgres_port: int = 5432

    @computed_field
    @property
    def database_url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                host=self.postgres_host,
                port=self.postgres_port,
                username=self.postgres_user,
                password=self.postgres_password,
                path=self.postgres_db
            )
        )
    
    @computed_field
    @property
    def sync_database_url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg2",
                host=self.postgres_host,
                port=self.postgres_port,
                username=self.postgres_user,
                password=self.postgres_password,
                path=self.postgres_db
            )
        )

@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
