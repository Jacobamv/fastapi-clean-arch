from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "FastAPI Clean Architecture"
    environment: str = "development"
    debug: bool = True

    database_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    log_destination: Literal["stdout", "file", "both"] = "stdout"
    log_file_path: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        sources = (init_settings, env_settings, file_secret_settings)
        if Path(".env").exists():
            sources = (init_settings, env_settings, dotenv_settings, file_secret_settings)
        return sources

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        if not value:
            raise ValueError("DATABASE_URL must be provided.")
        return value

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "title": self.project_name,
            "debug": self.debug,
        }

    @model_validator(mode="after")
    def validate_logging(self) -> "Settings":
        if self.log_destination in {"file", "both"} and not self.log_file_path:
            raise ValueError("LOG_FILE_PATH must be set when log_destination is 'file' or 'both'.")
        return self


@lru_cache()
def get_settings() -> Settings:
    return Settings()

