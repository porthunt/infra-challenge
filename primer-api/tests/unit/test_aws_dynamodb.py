import boto3
from moto import mock_dynamodb2
from tests.unit.mock_dynamodb import TRANSACTIONS
from app.aws import dynamodb
from app.settings import limit_settings, transaction_table


def generate_table(client):
    client.create_table(
        TableName=transaction_table,
        KeySchema=[
            {"AttributeName": "transaction_id", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "transaction_id",
                "AttributeType": "S",
            },
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 10,
        },
    )


def put_items(client):
    for t in TRANSACTIONS:
        client.put_item(
            TableName=transaction_table,
            Item={
                "transaction_id": {"S": t["transaction_id"]},
                "amount": {"N": str(t["amount"])},
                "merchant": {"S": t["merchant"]},
                "currency": {"S": t["currency"]},
                "date": {"S": t["date"]},
                "processor": {"S": t["processor"]},
            },
        )


@mock_dynamodb2
def test_retrieve_item():
    client = boto3.client("dynamodb", region_name="eu-west-1")
    generate_table(client)
    put_items(client)
    assert TRANSACTIONS[0] == dynamodb.retrieve_item(
        transaction_table, {"transaction_id": "xxx"}
    )


@mock_dynamodb2
def test_retrieve_item_not_found():
    client = boto3.client("dynamodb", region_name="eu-west-1")
    generate_table(client)
    assert not dynamodb.retrieve_item(
        transaction_table, {"transaction_id": "xxx"}
    )


@mock_dynamodb2
def test_retrieve_all():
    client = boto3.client("dynamodb", region_name="eu-west-1")
    generate_table(client)
    put_items(client)
    response = dynamodb.retrieve_all(transaction_table)
    assert len(response["Items"]) == 3
    assert response["limit"] == limit_settings["default"]


@mock_dynamodb2
def test_retrieve_all_empty():
    client = boto3.client("dynamodb", region_name="eu-west-1")
    generate_table(client)
    response = dynamodb.retrieve_all(transaction_table)
    assert len(response["Items"]) == 0
    assert response["limit"] == limit_settings["default"]


@mock_dynamodb2
def test_retrieve_all_limit():
    client = boto3.client("dynamodb", region_name="eu-west-1")
    generate_table(client)
    put_items(client)
    response = dynamodb.retrieve_all(transaction_table, limit=1)
    assert len(response["Items"]) == 1
    assert response["Items"][0] == TRANSACTIONS[0]
    assert response["limit"] == 1
    assert (
        response["LastEvaluatedKey"]["transaction_id"]
        == TRANSACTIONS[0]["transaction_id"]
    )


@mock_dynamodb2
def test_retrieve_all_cursor():
    client = boto3.client("dynamodb", region_name="eu-west-1")
    generate_table(client)
    put_items(client)
    response = dynamodb.retrieve_all(transaction_table, cursor="xxx")
    assert len(response["Items"]) == 2
    assert response["Items"] == TRANSACTIONS[1:]
    assert response["limit"] == limit_settings["default"]


@mock_dynamodb2
def test_retrieve_all_cursor_limit():
    client = boto3.client("dynamodb", region_name="eu-west-1")
    generate_table(client)
    put_items(client)
    response = dynamodb.retrieve_all(transaction_table, cursor="xxx", limit=1)
    assert len(response["Items"]) == 1
    assert response["limit"] == 1
    assert response["Items"][0] == TRANSACTIONS[1]
    assert response["LastEvaluatedKey"]["transaction_id"] == "yyy"
