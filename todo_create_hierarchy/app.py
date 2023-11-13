import boto3
import hierarchy
from dynamodb import DynamoDb
import os

TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb_handler = DynamoDb(boto3.resource("dynamodb").Table(TABLE_NAME))


def lambda_handler(event, _):
    counter: dict[str, int] = dynamodb_handler.get_item_count()

    return hierarchy.create(event_root=event["body"], options={"counter": counter})
