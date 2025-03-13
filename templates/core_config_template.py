from passlib.context import CryptContext

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

# from app.core.logger import setup_logger


class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    debug: bool = True
    secret_key: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()


# Database logger instance
# db_logger = setup_logger("database_logger", "logs/database_actions.log")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")