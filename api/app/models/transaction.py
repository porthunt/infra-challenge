import uuid
import random
from datetime import datetime
from pydantic import BaseModel, ValidationError, validator
from app.models.currency import Currency
from app.models.processor import Processor
from typing import List, Optional, Dict
from app.aws.dynamodb import retrieve_all, retrieve_item, put_item
from app.aws.sqs import send_message
from app.settings import transaction_table, transaction_dlq
from app.errors import (
    TransactionNotFoundError,
    InvalidTransactionDataError,
    TransactionConflictError,
)
from botocore.exceptions import ClientError


TRANSACTIONS_TO_POPULATE = 20


class Transaction(BaseModel):
    transaction_id: str
    date: str
    amount: int
    currency: Currency
    processor: Processor
    merchant: str

    @validator("date")
    def validate_date_format(cls, v):
        try:
            format = "%m/%d/%Y, %H:%M:%S"
            transaction_date = datetime.strptime(v, format)
            if transaction_date > datetime.now():
                raise InvalidTransactionDataError(
                    message="Invalid constraint: transaction "
                    "datetime after current time"
                )
        except ValueError:
            raise ValueError("Invalid date format")
        return v

    def to_json(self):
        return {
            "transaction_id": self.transaction_id,
            "date": self.date,
            "amount": self.amount,
            "currency": self.currency.value.upper(),
            "processor": self.processor.value.upper(),
            "merchant": self.merchant.lower(),
        }


def retrieve_transactions(
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    filters: Optional[List[Dict[str, str]]] = None,
) -> List[Transaction]:
    response = retrieve_all(
        transaction_table, limit=limit, cursor=cursor, filters=filters
    )
    data = {
        "transactions": [
            Transaction(
                transaction_id=item["transaction_id"],
                date=item["date"],
                amount=item["amount"],
                currency=Currency(value=item["currency"].upper()),
                processor=Processor(value=item["processor"].upper()),
                merchant=item["merchant"].upper(),
            ).to_json()
            for item in response["Items"]
        ],
        "limit": response["limit"],
    }

    if response.get("LastEvaluatedKey"):
        data["cursor"] = response["LastEvaluatedKey"]["transaction_id"]

    return data


def retrieve_transaction(transaction_id: str) -> Transaction:
    item = retrieve_item(transaction_table, {"transaction_id": transaction_id})

    if not item:
        raise TransactionNotFoundError(transaction_id=transaction_id)

    return Transaction(
        transaction_id=item["transaction_id"],
        date=item["date"],
        amount=item["amount"],
        currency=Currency(value=item["currency"].upper()),
        processor=Processor(value=item["processor"].upper()),
        merchant=item["merchant"].upper(),
    )


def create_transaction(item: Dict[str, str]):
    try:
        transaction = Transaction(
            transaction_id=item["transaction_id"],
            date=item["date"],
            amount=item["amount"],
            currency=Currency(value=item["currency"].upper()),
            processor=Processor(value=item["processor"].upper()),
            merchant=item["merchant"].upper(),
        )
        put_item(
            transaction_table,
            transaction.to_json(),
            item_hash_key="transaction_id",
        )
    except (ValidationError, ValueError, KeyError):
        send_message(transaction_dlq, item)
        raise InvalidTransactionDataError()
    except ClientError:
        send_message(transaction_dlq, item)
        raise TransactionConflictError()


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

    for _ in range(TRANSACTIONS_TO_POPULATE):
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
