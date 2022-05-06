import boto3
from app import utils
from app.settings import username
from app.models.transaction import retrieve_transactions, retrieve_transaction
from app.models.params import validate_params, TransactionsQueryParams


@utils.endpoint
def populate_table(event, context):
    client = boto3.resource("dynamodb")
    table = client.Table(f"{username}-transaction-challenge")
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
        data = retrieve_transactions(cursor=params.cursor, limit=params.limit)
        return data, 200
