from pydantic import BaseModel
from app.models.currency import Currency
from app.models.processor import Processor
from app.models.merchant import Merchant
from typing import List, Optional, Dict
from app.aws.dynamodb import retrieve_all, retrieve_item
from app.settings import transaction_table
from app.errors import TransactionNotFoundError


class Transaction(BaseModel):
    transaction_id: str
    date: str
    amount: int
    currency: Currency
    processor: Processor
    merchant: Merchant

    def to_json(self):
        return {
            "transaction_id": self.transaction_id,
            "date": self.date,
            "amount": self.amount,
            "currency": self.currency.value.upper(),
            "processor": self.processor.value.upper(),
            "merchant": self.merchant.value.upper(),
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
                merchant=Merchant(value=item["merchant"].upper()),
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
        merchant=Merchant(value=item["merchant"].upper()),
    )
