from typing import Dict, Optional, List
from app.settings import limit_settings

TRANSACTIONS = [
    {
        "transaction_id": "xxx",
        "amount": 1,
        "currency": "USD",
        "date": "05/05/2022, 18:13:21",
        "merchant": "socart",
        "processor": "INGENICO",
    },
    {
        "transaction_id": "yyy",
        "amount": 2,
        "currency": "GBP",
        "date": "05/05/2022, 18:13:21",
        "merchant": "mercity",
        "processor": "ADYEN",
    },
    {
        "transaction_id": "zzz",
        "amount": 3,
        "currency": "EUR",
        "date": "05/05/2022, 18:13:21",
        "merchant": "shopulse",
        "processor": "STRIPE",
    },
]


def retrieve_item(table: str, key: Dict[str, str]) -> Optional[Dict]:
    for t in TRANSACTIONS:
        if t["transaction_id"] == key["transaction_id"]:
            return t


def put_item(table: str, item: Dict[str, str]) -> Dict:
    pass


def retrieve_all(
    table: str,
    limit: Optional[int] = limit_settings["default"],
    cursor: Optional[str] = None,
    filters: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, str]:

    limit = limit if limit else limit_settings["default"]

    if limit and not cursor:
        return {"Items": TRANSACTIONS[:limit], "limit": limit}

    cursor_index = next(
        (
            idx
            for (idx, t) in enumerate(TRANSACTIONS)
            if t["transaction_id"] == cursor
        ),
        None,
    )

    response = {
        "Items": TRANSACTIONS[
            cursor_index + 1 : cursor_index + 1 + limit  # noqa
        ],
        "limit": limit,
    }

    if cursor_index < len(TRANSACTIONS):
        response["LastEvaluatedKey"] = {
            "transaction_id": TRANSACTIONS[cursor_index + 1]["transaction_id"]
        }

    return response
