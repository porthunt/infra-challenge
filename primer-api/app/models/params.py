from pydantic import BaseModel, conint, ValidationError, Extra
from app.settings import limit_settings
from typing import Optional, Dict, Type
from app.errors import InvalidInputError


class TransactionsQueryParams(BaseModel, extra=Extra.forbid):
    limit: conint(
        gt=limit_settings["min"], lt=limit_settings["max"] + 1
    ) = limit_settings["default"]
    cursor: Optional[str]
    merchant: Optional[str]


def validate_params(params: Dict[str, str], param_class: Type[BaseModel]):
    try:
        return param_class(**params)
    except ValidationError as e:
        error = e.errors()[0]
        raise InvalidInputError(message=f'{error["loc"][0]}: {error["msg"]}')
