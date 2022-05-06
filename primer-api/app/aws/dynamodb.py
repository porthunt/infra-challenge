import os
import boto3
from typing import Dict, Optional, List
from app.settings import limit_settings


def create_resource():
    region = os.getenv("AWS_REGION", "eu-west-1")
    return boto3.resource("dynamodb", region_name=region)


def retrieve_item(table_name: str, key: Dict) -> Optional[Dict]:
    resource = create_resource()
    table = resource.Table(table_name)
    item = table.get_item(Key=key)
    if item and item.get("Item"):
        return item.get("Item")


def retrieve_all(
    table_name: str,
    limit: Optional[int] = limit_settings["default"],
    cursor: Optional[str] = None,
) -> List[Dict]:
    args = {"Limit": limit if limit else limit_settings["default"]}
    if cursor:
        args["ExclusiveStartKey"] = {"transaction_id": cursor}

    resource = create_resource()
    table = resource.Table(table_name)
    response = table.scan(**args)
    response["limit"] = limit
    return response
