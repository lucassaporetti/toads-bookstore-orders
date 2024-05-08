import logging
from logging import config

from bookstore_orders.components.api.api import run_api
from bookstore_orders.components.config import LOGGING_CONFIG

config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()


class ToadsBookstoreOrders:
    @staticmethod
    def run(args=None):  # pylint: disable=unused-argument)
        """
        Main function: manager book orders.
        """
        logger.info(
            "Loading project toads-bookstore-orders..."
        )
        # create your start

        run_api()

        logger.info("Ended process")
