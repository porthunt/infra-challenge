import pytest
from app.models import transaction
from tests.unit.mock_dynamodb import retrieve_item, retrieve_all, put_item
from tests.unit.mock_sqs import send_message


@pytest.fixture
def transaction_mock(monkeypatch):
    monkeypatch.setattr(
        transaction,
        "retrieve_item",
        retrieve_item,
    )


@pytest.fixture
def transactions_mock(monkeypatch):
    monkeypatch.setattr(
        transaction,
        "retrieve_all",
        retrieve_all,
    )


@pytest.fixture
def add_transaction_mock(monkeypatch):
    monkeypatch.setattr(transaction, "put_item", put_item)


@pytest.fixture
def send_message_mock(monkeypatch):
    monkeypatch.setattr(transaction, "send_message", send_message)
