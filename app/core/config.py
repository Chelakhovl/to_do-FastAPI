from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Main application settings."""

    app_name: str = Field("To-Do API", env="APP_NAME")
    debug: bool = Field(True, env="DEBUG")
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    database_url: str = Field("sqlite:///./dev.db", env="DATABASE_URL")
    tz: str = Field("Europe/Kyiv", env="TZ")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
