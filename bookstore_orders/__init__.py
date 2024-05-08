from importlib.metadata import PackageNotFoundError, version  # type: ignore

from bookstore_orders.app import ToadsBookstoreOrders  # noqa # pylint: disable=unused-import

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
