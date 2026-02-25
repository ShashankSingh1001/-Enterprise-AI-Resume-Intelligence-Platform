from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str
    environment: str
    debug: bool

    # Server
    host: str
    port: int

    # Database
    database_url: str

    # MLflow
    mlflow_tracking_uri: str
    mlflow_experiment_name: str


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()