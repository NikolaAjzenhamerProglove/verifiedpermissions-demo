from resources import Resources
from boto3.dynamodb.conditions import Key


def _get_item(event_body: dict, resources: Resources) -> dict:
    return resources.dynamodb_table.get_item(Key={"id": event_body["id"]}).get(
        "Item", {}
    )


def _get_tasks_of_list(event_body: dict, resources: Resources) -> list[dict]:
    return resources.dynamodb_table.query(
        KeyConditionExpression=Key("parent_id").eq(event_body["list_id"]),
        IndexName="ParentChildrenIndex",
    ).get("Items", [])


def _get_board_children(event_body: dict, resources: Resources) -> list[dict]:
    return resources.dynamodb_table.query(
        KeyConditionExpression=(
            Key("board_id").eq(event_body["board_id"])
            & Key("path").begins_with(f"{event_body['board_id']}#")
        ),
        IndexName="FullLineageIndex",
    ).get("Items", [])


def _create_item(event_body: dict, resources: Resources) -> None:
    item = {
        "id": event_body["id"],
        "parent_id": event_body.get("parent_id", event_body["id"]),
        "board_id": event_body["board_id"],
        "path": event_body.get("path", f"{event_body['board_id']}#{event_body['id']}"),
        "name": event_body["name"],
        "type": event_body["type"],
    }
    resources.dynamodb_table.put_item(
        Item=item, ConditionExpression="attribute_not_exists(id)"
    )

    return item


def _create_items(event_body: dict, resources: Resources) -> None:
    items = []

    for event_item in event_body["items"]:
        item = _create_item(event_item, resources)
        items.append(item)

    return items


_REGISTERED_HANDLERS = {
    "GetItem": _get_item,
    "GetTasks": _get_tasks_of_list,
    "GetBoardChildren": _get_board_children,
    "CreateItem": _create_item,
    "CreateItems": _create_items,
}


def handle(event, resources: Resources):
    return _REGISTERED_HANDLERS[event["action"]](event["body"], resources)
