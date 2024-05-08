import logging
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from bookstore_orders.components.schemas.responses import BookOrderData
from bookstore_orders.components.models.book_order import BookOrder
from bookstore_orders.components.utils.database.service import DatabaseService
from bookstore_orders.components.utils.exceptions import APIException, DatabaseException

logger = logging.getLogger()


class Order:
    def __init__(self, user_id):
        self.user_id = user_id


class ABook(Order):
    def __init__(self, user_id):
        super().__init__(user_id)

    def get_book_order(self, major, minor):
        logger.info(f"Trying to get book order with major {major} and minor {minor} data.")

        with DatabaseService() as conn:
            try:
                logger.info("Getting book order from database.")
                book_order = (
                    conn.query(BookOrder)
                    .filter(BookOrder.user_id == self.user_id)
                    .filter(BookOrder.major_category == major)
                    .filter(BookOrder.minor_category == minor)
                    .one()
                )
                order_data = BookOrderData(
                    order_id=book_order.order_id,
                    book_id=book_order.book_id,
                    user_id=book_order.user_id,
                    quantity=book_order.quantity,
                    order_date_time=book_order.order_date_time,
                    order_status=book_order.order_status,
                    delivery_address=book_order.delivery_address,
                    payment_method=book_order.payment_method,
                    total_amount=book_order.total_amount,
                    order_notes=book_order.order_notes,
                    major_category=book_order.major_category,
                    minor_category=book_order.minor_category
                )
                return order_data.dict()
            except MultipleResultsFound as exc:
                logger.error(exc)
                raise APIException(
                    status_code=400,
                    message="Multiple results found",
                ) from exc
            except NoResultFound as exc:
                logger.error(exc)
                raise APIException(
                    status_code=404,
                    message="Book order not found with the given parameters",
                ) from exc
            except DatabaseException as exc:
                raise DatabaseException(
                    exc.status_code,
                    exc.message,
                ) from exc
