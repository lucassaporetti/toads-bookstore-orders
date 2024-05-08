import logging
from logging import config
from importlib.metadata import PackageNotFoundError, version  # type: ignore
import uvicorn
from fastapi import FastAPI

from app.components.api.exception_handlers import (
    include_exception_handlers,
)
from app.components.api.middleware import include_middleware
from app.components.api.routes import include_routes
from app.components.config import LOGGING_CONFIG, envs


config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/healthz") == -1


logging.getLogger("uvicorn.access").addFilter(EndpointFilter())


def api_factory():
    try:
        __version__ = version(__name__)
    except PackageNotFoundError:  # pragma: no cover
        __version__ = "0.1.0"

    app = FastAPI(
        title="Toads Bookstore",
        description="Bookstore test",
        version=__version__,
        docs_url="/swagger",
        redoc_url="/docs",
    )

    include_middleware(app, logger)
    include_exception_handlers(app, logger)
    include_routes(app, logger)

    logger.info("API load completed")

    return app


def run_api():
    app = api_factory()
    uvicorn.run(app, host=envs.HOST_IP, port=envs.HOST_PORT, debug=True)
