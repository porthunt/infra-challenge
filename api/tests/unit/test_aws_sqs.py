import boto3
from moto import mock_sqs
from app.aws import sqs


@mock_sqs
def test_send_message():
    resource = boto3.resource(
        "sqs",
        region_name="eu-west-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    queue_name = "test"
    queue = resource.create_queue(QueueName=queue_name)
    assert len(queue.receive_messages()) == 0
    sqs.send_message(queue_name, {"foo": "bar"})
    assert len(queue.receive_messages()) == 1
