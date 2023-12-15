from copy import deepcopy
from typing import Optional
from boto3_resources import Boto3Resources

NAMESPACE = "TODO"


def _get_item_from_event(resource_id: str, bt3: Boto3Resources) -> Optional[dict]:
    return bt3.dynamodb_table.get_item(Key={"id": resource_id}).get("Item")


def _create_resource_entity_identifier(entity_id: str) -> dict:
    entity_type: str

    if entity_id.startswith("B"):
        entity_type = f"{NAMESPACE}::Board"
    elif entity_id.startswith("L"):
        entity_type = f"{NAMESPACE}::List"
    else:
        entity_type = f"{NAMESPACE}::Task"

    return {
        "entityType": entity_type,
        "entityId": entity_id,
    }


def _create_resource_entities(path: str) -> list[dict]:
    entities = []
    path = path.split("#")

    for entity_id in path:
        entity = {
            "identifier": _create_resource_entity_identifier(entity_id),
            "parents": deepcopy(
                list(map(lambda entity: entity["identifier"], entities))
            ),
        }

        entities.append(entity)

    return entities


def can_execute(event: dict, bt3: Boto3Resources) -> bool:
    if not bt3.PERMISSIONS_ENABLED:
        return True

    principal_id = event["username"]
    action_id = event["action"]
    resource_id = event["body"]["id"]

    # We retrieve item from the database to get the path of the resource
    item: Optional[dict] = _get_item_from_event(resource_id=resource_id, bt3=bt3)
    # We build the parent tree for the resource
    entities = _create_resource_entities(item["path"])

    response = bt3.verifiedpermissions.is_authorized(
        policyStoreId=bt3.POLICY_STORE_ID,
        principal={
            "entityType": f"{NAMESPACE}::User",
            "entityId": principal_id,
        },
        action={
            "actionType": f"{NAMESPACE}::Action",
            "actionId": action_id,
        },
        resource=_create_resource_entity_identifier(resource_id),
        entities={
            "entityList": entities,
        },
    )

    return response["decision"] == "ALLOW"
