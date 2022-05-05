import boto3
from app.utils import endpoint, populate, get_params, get_query_params
from app.settings import username
from app.models.transaction import retrieve_transactions, retrieve_transaction


@endpoint
def populate_table(event, context):
    client = boto3.resource("dynamodb")
    table = client.Table(f"{username}-transaction-challenge")
    populate(table)
    return {"message": "transaction table populated"}, 200


@endpoint
def transactions(event, context):
    params = get_params(event)
    query_params = get_query_params(event)
    transaction_id = params.get("id")
    # merchant = query_params.get("merchant")

    if transaction_id:
        transaction = retrieve_transaction(transaction_id)
        return transaction.to_json(), 200
    else:
        transactions = retrieve_transactions()
        return [transaction.to_json() for transaction in transactions], 200
