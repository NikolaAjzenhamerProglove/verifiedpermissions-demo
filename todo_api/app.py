import os
import boto3
import handlers
from resources import Resources

TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb_table = boto3.resource("dynamodb").Table(TABLE_NAME)
verifiedpermissions = boto3.client("verifiedpermissions")


def lambda_handler(event, _):
    return handlers.handle(event, Resources(dynamodb_table, verifiedpermissions))
