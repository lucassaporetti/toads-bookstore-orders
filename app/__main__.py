from app.app import ToadsBookstoreOrders  # pragma: no cover
from app.components.utils.arg_parser import ArgParse  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    args = ArgParse().set_parser()  # pragma: no cover
    ToadsBookstoreOrders.run(args)  # pragma: no cover
