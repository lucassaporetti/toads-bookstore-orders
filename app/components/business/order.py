import logging

from app.components.schemas.responses import BookOrderData

logger = logging.getLogger()


class Order:
    def __init__(self, user_id):
        self.user_id = user_id

    class ABook:
        @staticmethod
        def get_book_order(major, minor):
            logger.info(f"Trying to get book order with major {major} and minor {minor} data...")
            book_order_data = BookOrderData()
            return book_order_data
