import logging
import uuid

from bookstore_orders.components.schemas.responses import BookOrderData

logger = logging.getLogger()


class Order:
    def __init__(self, user_id):
        self.user_id = user_id

    class ABook:
        @staticmethod
        def get_book_order(major, minor):
            logger.info(f"Trying to get book order with major {major} and minor {minor} data...")
            order_data = BookOrderData(
                order_id=str(uuid.uuid4()),
                book_id="123456",
                user_id="789",
                quantity=2,
                order_status="pending",
                delivery_address="Rua dos Bobos, 0",
                payment_method="credit_card",
                total_amount=50.0,
                order_notes="Por favor, entregue antes das 18:00",
                major_category="Ficção",
                minor_category="Romance"
            )
            book_order_data = order_data.dict()
            return book_order_data
