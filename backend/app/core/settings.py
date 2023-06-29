from typing import Optional

from pydantic import BaseSettings, PostgresDsn


class _Settings(BaseSettings):
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


class _UvicornSettings(BaseSettings):
    workers: Optional[int] = None
    port = 8000
    host = "localhost"

    class Config:
        env_file = ".env"
        env_prefix = "uvicorn_"


class _AppSettings(BaseSettings):
    local_run: bool = True
    show_swagger: bool = True
    allowed_origins_regex: str = "^.+$"

    data_offset: int = 0

    class Config:
        env_file = ".env"
        env_prefix = "app_"


class _DBSettings(BaseSettings):
    dsn: Optional[PostgresDsn] = None
    autocommit: bool = False

    class Config:
        env_file = ".env"
        env_prefix = "db_"


db_settings = _DBSettings()
settings = _Settings()
app_settings = _AppSettings()
uvicorn_settings = _UvicornSettings()
