from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment or .env file."""
    DATABASE_URL: str = "sqlite:///./db.sqlite3"
    SECRET_KEY: str = "change-me"

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()

