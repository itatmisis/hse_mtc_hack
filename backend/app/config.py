from loguru import logger
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseSettings, PostgresDsn, validator
from dotenv import load_dotenv

log = logger


load_dotenv()


class Settings(BaseSettings):
    DOCKER_MODE: bool = False
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # TG_SERVICE_HOST: str
    # TG_SERVICE_PORT: int

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=str(values.get("POSTGRES_SERVER"))
            if values.get("POSTGRES_SERVER")
            else "127.0.0.1",
            port="5432",
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file_encoding = "utf-8"
        env_file = ".env"


settings = Settings()  # type: ignore
