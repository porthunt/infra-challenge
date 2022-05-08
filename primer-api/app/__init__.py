import boto3
import json
from app import utils
from app.settings import transaction_table, logger
from app.models.transaction import (
    retrieve_transactions,
    retrieve_transaction,
    create_transaction,
)
from app.models.params import validate_params, TransactionsQueryParams
from app.errors import InvalidTransactionDataError


@utils.endpoint
def populate_table(event, context):
    client = boto3.resource("dynamodb")
    table = client.Table(transaction_table)
    utils.populate(table)
    return {"message": "transaction table populated"}, 200


@utils.endpoint
def transactions(event, context):
    params = utils.get_params(event)
    query_params = utils.get_query_params(event)
    transaction_id = params.get("id")
    params = validate_params(query_params, TransactionsQueryParams)

    if transaction_id:
        transaction = retrieve_transaction(transaction_id)
        return transaction.to_json(), 200
    else:
        data = retrieve_transactions(
            cursor=params.cursor, limit=params.limit, filters=params.filters()
        )
        return data, 200


def add_transaction(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])
        try:
            create_transaction(body)
        except InvalidTransactionDataError:
            logger.error(f'Can\'t add the following record: {record["body"]}')
    return None, 200
