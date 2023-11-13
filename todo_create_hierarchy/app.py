from typing import Optional
import boto3
import hierarchy
from dynamodb import DynamoDb
import os

TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb_handler = DynamoDb(boto3.resource("dynamodb").Table(TABLE_NAME))


def lambda_handler(event, _):
    """
    Event example:

    {
        "body": {
            "name": "My Board 1",
            "type": "B",
            "items": [
                {
                    "name": "My List 1",
                    "type": "L",
                    "items": [
                        {
                            "name": "My Task 1.1",
                            "type": "T"
                        },
                        {
                            "name": "My Task 1.2",
                            "type": "T"
                        }
                    ]
                },
                {
                    "name": "My List 2",
                    "type": "L",
                    "items": [
                        {
                            "name": "My Task 2.1",
                            "type": "T"
                        },
                        {
                            "name": "My Task 2.2",
                            "type": "T"
                        }
                    ]
                },
            ]
        }
    }
    """
    counter: dict[str, int] = dynamodb_handler.get_item_count()

    return hierarchy.create(event_root=event["body"], options={"counter": counter})
