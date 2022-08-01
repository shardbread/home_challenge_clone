from functools import lru_cache
from typing import (
    Optional,
    Any,
)

from pydantic import (
    BaseSettings,
    PostgresDsn,
)


class CommonConfig(BaseSettings):
    """
        The main config file
    """
    API_HOST: str = ""
    API_PORT: int = 8080

    SWAGGER_ENABLED: bool = False
    ENV_NAME: str = "dev"

    # DB
    DATABASE_URL: Optional[
        PostgresDsn
    ] = "postgresql://postgresql:postgresql@db:5432/storage"
    DB_ECHO_LOG: bool = False
    DB_POOL_SIZE: int = 20
    DB_POOL_RECYCLE: int = 300
    DB_TIMEOUT: int = 30
    DEFAULT_LIMIT: int = 100

    PREFIX_DELIMITER: str = "_"

    @property
    def async_database_url(self) -> Optional[str]:
        return (
            self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
            if self.DATABASE_URL
            else self.DATABASE_URL
        )


settings_classes = {
    "common": CommonConfig,
}


@lru_cache
def get_settings():
    return settings_classes["common"]()


settings = get_settings()


def get_swagger_settings() -> dict[str, Any]:
    swagger_settings = {
        True: dict(
            docs_url="/docs/",
            openapi_url="/docs/openapi.json",
        ),
        False: dict(docs_url=None, openapi_url=None, redoc_url=None)
    }

    return swagger_settings[settings.SWAGGER_ENABLED]
