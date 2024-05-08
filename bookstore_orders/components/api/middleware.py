from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


def include_middleware(app, logger):
    logger.info("loading middleware handler")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_credentials=True,
        allow_headers=["*"],
    )

    @app.exception_handler(ValueError)
    async def validation_exception_handler(
        request: Request, exception: ValueError
    ):  # pylint: disable=unused-argument # pragma: no cover
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "message": "Invalid Request field",
                "error": str(exception),
            },
        )
