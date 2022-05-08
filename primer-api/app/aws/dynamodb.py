import os
import boto3
from typing import Dict, Optional, List, Tuple
from app.settings import limit_settings
from boto3.dynamodb.conditions import And, Key
from functools import reduce


def create_resource():
    region = os.getenv("AWS_REGION", "eu-west-1")
    return boto3.resource("dynamodb", region_name=region)


def retrieve_item(table_name: str, key: Dict) -> Optional[Dict]:
    resource = create_resource()
    table = resource.Table(table_name)
    item = table.get_item(Key=key)
    if item and item.get("Item"):
        return item.get("Item")


def put_item(
    table_name: str,
    item: Dict,
    allow_update: bool = False,
    item_hash_key: str = None,
) -> Dict:
    if not allow_update and not item_hash_key:
        raise AttributeError(
            "If allow_update is False, item_hash_key must be set"
        )
    resource = create_resource()
    table = resource.Table(table_name)
    args = {"Item": item}
    if not allow_update:
        args["ConditionExpression"] = f"attribute_not_exists({item_hash_key})"
    response = table.put_item(**args)
    return response


def retrieve_all(
    table_name: str,
    limit: Optional[int] = limit_settings["default"],
    cursor: Optional[str] = None,
    filters: Optional[List[Dict[str, str]]] = None,
) -> List[Dict]:
    args = {"Limit": limit if limit else limit_settings["default"]}
    if cursor:
        args["ExclusiveStartKey"] = {"transaction_id": cursor}
    if filters:
        __filters = prepare_filters(filters)
        args["FilterExpression"] = (
            __filters[0] if len(__filters) == 1 else reduce(And, __filters)
        )

    resource = create_resource()
    table = resource.Table(table_name)
    response = table.scan(**args)
    response["limit"] = limit
    return response


def prepare_filters(filters: List[Dict[str, str]]) -> Tuple[Key]:
    __filters = []
    for filter in filters:
        operator = filter.get("operator", "eq")
        if operator == "eq":
            attr = Key(filter["key"]).eq(filter["value"])
        elif operator == "gte":
            attr = Key(filter["key"]).gt(filter["value"])
        elif operator == "lte":
            attr = Key(filter["key"]).lt(filter["value"])
        __filters.append(attr)
    return tuple(__filters)
