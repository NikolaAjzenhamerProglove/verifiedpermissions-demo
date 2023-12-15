import boto3
import os
from uuid import uuid4
from aws_lambda_powertools.logging import Logger

logger = Logger()

POLICY_STORE_ID = os.environ["POLICY_STORE_ID"]
RESOURCE_ENTITY_TYPE_MAP = {
    "B": "Board",
    "L": "List",
    "T": "Task",
}

verifiedpermissions = boto3.client("verifiedpermissions")


@logger.inject_lambda_context(log_event=True, clear_state=True)
def lambda_handler(event: dict, _):
    username: str = event["username"]
    action: str = event["action"]
    resource: str = event["resource"]
    allow: bool = event["allow"]

    statement = ("permit" if allow else "forbid") + "(" + \
        f"principal == TODO::User::\"{username}\"," + \
        f"action    == TODO::Action::\"{action}\"," + \
        f"resource  == TODO::{RESOURCE_ENTITY_TYPE_MAP[resource[0]]}::\"{resource}\"" + \
    ");"
    
    description: str = ("Allow" if allow else "Deny") + f" {username} to perform {action} on {resource}"
    client_token = str(uuid4())

    logger.append_keys(statement=statement, description=description, client_token=client_token)
    logger.info("Creating policy")

    response: dict = verifiedpermissions.create_policy(
        clientToken=client_token,
        definition={  
            "static": {
                "statement": statement,
                "description": description,
            }
        },
        policyStoreId=POLICY_STORE_ID
    )

    return response["policyId"]
