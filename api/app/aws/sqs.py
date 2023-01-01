import os
import boto3
import json
from typing import Dict


def create_resource():
    region = os.getenv("AWS_REGION", "eu-west-1")
    return boto3.resource("sqs", region_name=region)


def send_message(queue_name: str, message: Dict) -> str:
    resource = create_resource()
    body = json.dumps(message)
    queue = resource.get_queue_by_name(QueueName=queue_name)
    response = queue.send_message(MessageBody=body)
    return response.get("MessageId")
