from pydantic import BaseModel, conint, ValidationError, Extra, Field
from app.settings import limit_settings
from typing import Optional, Dict, Type
from app.errors import InvalidInputError


class TransactionsQueryParams(BaseModel, extra=Extra.forbid):
    limit: conint(
        gt=limit_settings["min"], lt=limit_settings["max"] + 1
    ) = limit_settings["default"]
    cursor: Optional[str]
    merchant: Optional[str]
    processor: Optional[str]
    currency: Optional[str]
    amount: Optional[str] = Field(
        regex=r"^((gte|lte):)?\d+$",
        description="Format should be [gte|lte]:[int]",
    )

    def filters(self) -> Dict[str, str]:
        response = []
        if self.merchant:
            response.append(
                {"key": "merchant", "value": self.merchant.lower()}
            )
        if self.processor:
            response.append(
                {"key": "processor", "value": self.processor.upper()}
            )
        if self.currency:
            response.append(
                {"key": "currency", "value": self.currency.upper()}
            )
        if self.amount:
            amount = self.amount.split(":")
            entry = {"key": "amount"}
            if len(amount) == 2:
                entry["operator"] = amount[0]
                entry["value"] = int(amount[1])
            else:
                entry["value"] = int(amount[0])
            response.append(entry)
        return response


def validate_params(params: Dict[str, str], param_class: Type[BaseModel]):
    try:
        return param_class(**params)
    except ValidationError as e:
        error = e.errors()[0]
        raise InvalidInputError(message=f'{error["loc"][0]}: {error["msg"]}')
