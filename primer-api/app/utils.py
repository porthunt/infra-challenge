import uuid
import random
import json
from datetime import datetime
from typing import Callable
from app.settings import logger
from app.errors import Error, UnexpectedError


def populate(table):
    processors = [
        "BRAINTREE",
        "ADYEN",
        "STRIPE",
        "PAYPAL",
        "GOCARDLESS",
        "INGENICO",
    ]
    currencies = ["GBP", "USD", "EUR"]
    merchants = ["mercity", "shopulse", "socart", "bransport"]

    for _ in range(100):
        entry = {
            "transaction_id": str(uuid.uuid4()),
            "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "amount": random.randrange(1, 4000),
            "currency": random.choice(currencies),
            "processor": random.choice(processors),
            "merchant": random.choice(merchants),
        }
        table.put_item(Item=entry)
    return True


def endpoint(func: Callable):
    def wrapper(event, context=None):
        try:
            body, status_code = func(event, context)
        except Exception as e:
            logger.exception(e)
            if not issubclass(e.__class__, Error):
                e = UnexpectedError()
            body = e.to_json()
            status_code = e.status_code
        return {"statusCode": status_code, "body": json.dumps(body)}

    return wrapper


def get_params(event):
    params = event["pathParameters"]
    return params if params else {}


def get_payload(event):
    body = json.loads(event["body"])
    return body if body else {}


def get_query_params(event):
    params = event.get("queryStringParameters")
    return params if params else {}
