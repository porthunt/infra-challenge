import os
import logging


def retrieve_log_level():
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
    }
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    try:
        return log_levels[log_level]
    except KeyError:
        logger.error(f"Log level {log_level} is invalid")


logging.basicConfig(
    format="[%(levelname)s] :: %(message)s", level=retrieve_log_level()
)
logger = logging.getLogger("infra-challenge")
transaction_table = os.getenv(
    "TRANSACTION_TABLE", "porthunt-transaction-challenge"
)
transaction_dlq = os.getenv(
    "TRANSACTION_DLQ", "porthunt-infra-challenge-queue-DLQ"
)
limit_settings = {"default": 100, "min": 1, "max": 1000}
