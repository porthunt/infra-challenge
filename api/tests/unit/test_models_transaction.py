import pytest
from app.models import transaction
from app.errors import TransactionNotFoundError, InvalidTransactionDataError
from app.settings import limit_settings
from datetime import datetime
from dateutil.relativedelta import relativedelta


def test_retrieve_transactions(transactions_mock):
    items = transaction.retrieve_transactions()
    assert len(items["transactions"]) == 3
    assert items["transactions"][0]["transaction_id"] == "xxx"
    assert items["transactions"][1]["transaction_id"] == "yyy"
    assert items["transactions"][2]["transaction_id"] == "zzz"
    assert items["limit"] == limit_settings["default"]
    assert not items.get("cursor")


def test_retrieve_transactions_cursor(transactions_mock):
    items = transaction.retrieve_transactions(cursor="yyy")
    assert len(items["transactions"]) == 1
    assert items["transactions"][0]["transaction_id"] == "zzz"
    assert items["limit"] == limit_settings["default"]
    assert items["cursor"] == "zzz"


def test_retrieve_transactions_limit_and_cursor(transactions_mock):
    items = transaction.retrieve_transactions(limit=1, cursor="xxx")
    assert len(items["transactions"]) == 1
    assert items["transactions"][0]["transaction_id"] == "yyy"
    assert items["limit"] == 1
    assert items["cursor"] == "yyy"


def test_retrieve_transaction(transaction_mock):
    item = transaction.retrieve_transaction("xxx")
    assert type(item) == transaction.Transaction
    assert item.amount == 1
    assert item.currency.value == "USD"
    assert item.merchant == "FOO"
    assert item.processor.value == "INGENICO"


def test_retrieve_inexistent_transaction(transaction_mock):
    with pytest.raises(TransactionNotFoundError):
        transaction.retrieve_transaction("aaa")


def test_create_transaction(add_transaction_mock, send_message_mock):
    transaction.create_transaction(
        {
            "transaction_id": "foobar",
            "date": "05/07/2022, 23:55:32",
            "merchant": "socart",
            "currency": "USD",
            "processor": "stripe",
            "amount": 400,
        }
    )


def test_create_transaction_invalid_currency(
    add_transaction_mock, send_message_mock
):
    with pytest.raises(InvalidTransactionDataError):
        transaction.create_transaction(
            {
                "transaction_id": "foobar",
                "date": "05/07/2022, 23:55:32",
                "merchant": "socart",
                "currency": "BRL",
                "processor": "stripe",
                "amount": 400,
            }
        )


def test_create_transaction_invalid_processor(
    add_transaction_mock, send_message_mock
):
    with pytest.raises(InvalidTransactionDataError):
        transaction.create_transaction(
            {
                "transaction_id": "foobar",
                "date": "05/07/2022, 23:55:32",
                "merchant": "socart",
                "currency": "USD",
                "processor": "processorA",
                "amount": 400,
            }
        )


def test_create_transaction_invalid_body(
    add_transaction_mock, send_message_mock
):
    with pytest.raises(InvalidTransactionDataError):
        transaction.create_transaction(
            {
                "transaction_id": "foobar",
            }
        )


def test_create_transaction_invalid_date(
    add_transaction_mock, send_message_mock
):
    date = datetime.now() + relativedelta(years=2)
    with pytest.raises(InvalidTransactionDataError):
        transaction.create_transaction(
            {
                "transaction_id": "foobar",
                "date": date.strftime("%m/%d/%Y, %H:%M:%S"),
                "merchant": "socart",
                "currency": "USD",
                "processor": "stripe",
                "amount": 400,
            }
        )
