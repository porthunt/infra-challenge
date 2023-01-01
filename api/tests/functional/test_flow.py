import requests
from app.aws.dynamodb import retrieve_all
from app.models.transaction import TRANSACTIONS_TO_POPULATE
from app.settings import transaction_table


def test_populate(url):
    before = len(retrieve_all(transaction_table)["Items"])
    response = requests.post(f"{url}/populate")
    assert response.status_code == 200
    now = len(retrieve_all(transaction_table)["Items"])
    assert before + TRANSACTIONS_TO_POPULATE == now


def test_retrieve_transactions(url, api_key):
    dynamo_items = retrieve_all(transaction_table)["Items"]
    response = requests.get(
        f"{url}/transactions?limit=1000", headers={"x-api-key": api_key}
    )
    assert response.status_code == 200
    if len(dynamo_items) > 0:
        assert len(response.json()) > 0


def test_retrieve_transaction(url, api_key):
    dynamo_items = retrieve_all(transaction_table)["Items"]
    transaction = dynamo_items[0]
    response = requests.get(
        f"{url}/transactions/{transaction['transaction_id']}",
        headers={"x-api-key": api_key},
    )
    assert response.status_code == 200
    assert transaction == response.json()
