import os
import boto3
from typing import Dict, Optional, List


def create_resource():
    region = os.getenv("AWS_REGION", "eu-west-1")
    return boto3.resource("dynamodb", region_name=region)


def retrieve_item(table_name: str, key: Dict) -> Optional[Dict]:
    resource = create_resource()
    table = resource.Table(table_name)
    item = table.get_item(Key=key)
    if item and item.get("Item"):
        return item.get("Item")


def retrieve_all(table_name: str) -> List[Dict]:
    resource = create_resource()
    table = resource.Table(table_name)
    response = table.scan()
    return response["Items"]
