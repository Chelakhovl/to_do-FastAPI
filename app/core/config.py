from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Main application settings."""

    app_name: str = Field(default="To-Do API")
    debug: bool = Field(default=True)
    redis_url: str = Field(default="redis://localhost:6379/0")
    database_url: str = Field(default="sqlite:///./dev.db")
    tz: str = Field(default="Europe/Kyiv")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
