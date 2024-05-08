from pathlib import Path
from pydantic import BaseSettings

BASE_PROJECT = Path(__file__).resolve(strict=True).parent.parent

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "app": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


class Envs(BaseSettings):
    HOST_IP: str = "127.0.0.1"
    HOST_PORT: int = 8001
    APPLICATION_NAME: str = "ToadsBookstoreOrders"

    # DB CONFIG
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_DATABASE: str = "toads_bookstore"
    DB_SERVICE: str = "postgresql"
    SQLALCHEMY_ECHO: bool = False

    # REGISTRATION CONFIG
    REGISTRATION_SERVICE_URL: str = "http://localhost:8001"
    REGISTRATION_GET_USER_ENDPOINT: str = "/get-user-with-cpf/"

    class Config:
        case_sensitive = True


envs = Envs()
