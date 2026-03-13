from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # DB
    sqlalchemy_database_url: str = "mysql+mysqlconnector://root:123456@localhost:3306/dynamic_qr_marketing"

    # JWT
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",  # tranh loi extra_forbidden neu .env co key khac
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()