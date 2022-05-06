import pytest
from app.models import transaction
from tests.unit.mock_dynamodb import retrieve_item, retrieve_all


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
