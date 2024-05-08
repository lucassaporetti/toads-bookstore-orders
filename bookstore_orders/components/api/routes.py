from fastapi import APIRouter, Header
from fastapi.responses import RedirectResponse
import jwt

from bookstore_orders.components.schemas.monitoring import Healthz
from bookstore_orders.components.schemas.responses import (
    BookOrderData
)
from bookstore_orders.components.business.order import Order


def include_routes(app, logger):
    logger.info("loading routes ")

    router = APIRouter()

    @app.get("/", include_in_schema=False)
    async def redirect_to_swagger():
        return RedirectResponse("/swagger")

    @router.get("/healthz", response_model=Healthz, include_in_schema=False)
    async def healthz():
        return Healthz()

    @router.get(
        "/orders/book/{major}/{minor}",
        response_model=BookOrderData,
        summary="Get book order",
        description="Get book order data according to major (main category) and minor (subcategory) parameters",
    )
    async def get_book_order(major: str, minor: str, authorization=Header(default=None)):
        claims = jwt.decode(
            authorization.replace("Bearer ", ""), options={"verify_signature": False}
        )
        user_id = claims["user_id"]
        return Order(user_id).ABook().get_book_order(major=major, minor=minor)

    app.include_router(router)
