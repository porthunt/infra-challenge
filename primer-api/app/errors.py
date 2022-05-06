from app.settings import logger


class Error(Exception):

    default_message = ""

    def __init__(self, message=None, **kwargs):
        Exception.__init__(self)
        self.message = (
            message if message else self.default_message.format(**kwargs)
        )
        logger.error(self.message)

    def __str__(self):
        return self.message

    def to_json(self):
        response = {
            "message": self.message,
            "status_code": self.status_code,
        }
        return response


class UnexpectedError(Error):
    status_code = 500
    default_message = "Unexpected error"


class TransactionNotFoundError(Error):
    status_code = 404
    default_message = "Transaction '{transaction_id}' not found"


class InvalidInputError(Error):
    status_code = 400
    default_message = "Invalid input"
