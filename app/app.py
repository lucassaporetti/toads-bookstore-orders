import logging
from logging import config

from app.components.api.api import run_api
from app.components.config import LOGGING_CONFIG, envs

config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()


class ToadsBookstoreOrders:
    @staticmethod
    def run(args=None):  # pylint: disable=unused-argument)

        """
        Main function: working with book orders.
        """

        logger.info(
            f"Loading project ToadsBookstoreOrders, Environment {envs.ENVIRONMENT}"
        )

        run_api()

        logger.info("Ended process")
