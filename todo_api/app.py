import os
import boto3
import handlers
from boto3_resources import Boto3Resources
import permissions

TABLE_NAME = os.environ["TABLE_NAME"]
POLICY_STORE_ID = os.environ["POLICY_STORE_ID"]
PERMISSIONS_ENABLED = os.environ["PERMISSIONS_ENABLED"] == "true"

dynamodb_table = boto3.resource("dynamodb").Table(TABLE_NAME)
verifiedpermissions = boto3.client("verifiedpermissions")


bt3 = Boto3Resources(
    dynamodb_table=dynamodb_table,
    verifiedpermissions=verifiedpermissions,
    POLICY_STORE_ID=POLICY_STORE_ID,
    PERMISSIONS_ENABLED=PERMISSIONS_ENABLED,
)


def lambda_handler(event, _):
    if not permissions.can_execute(event=event, bt3=bt3):
        return {
            "statusCode": 403,
            "body": "User is not authorized to perform this action",
        }

    return handlers.handle(event=event, bt3=bt3)
