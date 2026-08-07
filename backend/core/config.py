from logging.config import dictConfig
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent



class BaseConfig(BaseSettings):
    """
    Базовая настройка c подключением env
    """

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf_8",
        extra="allow"
    )


class AppConfig(BaseConfig):
    """
    Настройки для приложения
    """



class AsyncPGConfig(BaseConfig):
    """
    Настройки для БД
    """

    PG_USER: str= "postgres"
    PG_PASSWORD: str = ""
    PG_DB: str ="postgres"
    PG_HOST: str = "localhost"
    PG_PORT:int = 5432

class AuthConfig(BaseConfig):
    """
    Настройки авторизации
    """
    ...

class LoggConfig(BaseConfig):
    """
    Настройки логирования.
    """

    LOG_LEVEL: str

    @property
    def logging_config(self):
        return {
            "version:":1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "level": self.LOG_LEVEL,
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                },
            },
            "root": {
                "level": self.LOG_LEVEL,
                "handlers": ["default"],
            },
            "loggers": {
                "uvicorn": {"level": self.LOG_LEVEL},
                "uvicorn.error": {"level": self.LOG_LEVEL},
                "uvicorn.access": {
                    "level": self.LOG_LEVEL,
                    "propagate": True,
                    "handlers": ["default"],
                },
            },
        }

    #TODO: добавить туда где запускать будем, Лёш не забудь
    def setup_logging(self):
        dictConfig(self.logging_config)

class Config:
    log_config: LoggConfig = LoggConfig()
    app_config: AppConfig = AppConfig()
    postgres_config: AsyncPGConfig = AsyncPGConfig()
    auth_config: AuthConfig = AuthConfig()

config = Config()


