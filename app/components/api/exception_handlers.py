from datetime import datetime
from uuid import uuid4
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.components.utils.exceptions import APIException


def include_exception_handlers(app, logger):
    logger.info("loading exception handler")

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exception: HTTPException  # pylint: disable=unused-argument
    ):  # pragma: no cover
        return JSONResponse(
            status_code=exception.status_code,
            content={
                "status": exception.status_code,
                "message": exception.detail,
            },
        )

    @app.exception_handler(APIException)
    async def http_api_exception_handler(
        request: Request, exception: APIException  # pylint: disable=unused-argument
    ):  # pragma: no cover
        return JSONResponse(
            status_code=exception.status_code,
            content={
                "timestamp": str(datetime.now()),
                "status": exception.status_code,
                "error": exception.error,
                "message": exception.message,
                "method": request.method,
                "path": request.url.path,
                "error_details": {
                    "unique_id": str(uuid4()),
                    "message": exception.message,
                },
            },
        )
