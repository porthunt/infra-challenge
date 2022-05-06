import pytest
from app.models import transaction
from app.errors import TransactionNotFoundError
from app.settings import limit_settings


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
    assert item.merchant.value == "SOCART"
    assert item.processor.value == "INGENICO"


def test_retrieve_inexistent_transaction(transaction_mock):
    with pytest.raises(TransactionNotFoundError):
        transaction.retrieve_transaction("aaa")
