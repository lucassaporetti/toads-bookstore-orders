from http.client import responses
from uuid import uuid4


class ErrorDetails:
    def __init__(self, message: str, unique_id: str = str(uuid4())):
        self.message = message
        self.unique_id = unique_id

    def to_dict(self):
        return {"unique_id": self.unique_id, "message": self.message}


class APIException(Exception):  # pragma: no cover
    def __init__(self, status_code: int, message: str, error_details: list):
        self.message = message
        self.status_code = status_code
        self.error = responses[status_code]
        self.error_details = error_details
        super().__init__(self.status_code, self.message)


class DatabaseException(Exception):  # pragma: no cover
    def __init__(self, status: int, message: str):
        self.status_code = status
        self.message = message
        super().__init__(self.status_code, self.message)


class UpdateTableException(DatabaseException):  # pragma: no cover
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(self.status_code, self.message)


class ToadsBookstoreOrdersException(Exception):  # pragma: no cover
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code, message)
        self.status_code = status_code
        self.message = message
