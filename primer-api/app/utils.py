import json
from typing import Callable
from app.settings import logger
from app.errors import Error, UnexpectedError


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
