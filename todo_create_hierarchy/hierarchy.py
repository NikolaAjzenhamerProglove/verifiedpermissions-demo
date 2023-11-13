from typing import Optional


_MAP = {
    "B": "BOARD",
    "L": "LIST",
    "T": "TASK",
}


def _abbr_to_type(abbr: str) -> str:
    return _MAP[abbr]


def _create_id(abbr: str, options: dict) -> str:
    options["counter"][abbr] += 1
    return f"{abbr}-{options['counter'][abbr]}"


def _create_item(
    id: str, board_id: str, name: str, abbr: str, parent: Optional[dict] = None
):
    return {
        "id": id,
        "parent_id": f"{parent['id'] if parent else id}",
        "board_id": board_id,
        "path": parent["path"] + "#" + id if parent else board_id,
        "name": name,
        "type": _abbr_to_type(abbr=abbr),
    }


def _process_items(
    event_items: list[dict],
    response_items: list[dict],
    board_id: str,
    options: dict,
    root: Optional[dict] = None,
) -> None:
    for event_item in event_items:
        item = _create_item(
            id=_create_id(event_item["type"], options),
            board_id=board_id,
            name=event_item["name"],
            abbr=event_item["type"],
            parent=root,
        )
        response_items.append(item)

        _process_items(
            event_items=event_item.get("items", []),
            response_items=response_items,
            board_id=board_id,
            options=options,
            root=item,
        )


def create(event_root: dict, options: dict):
    items_in_hierarchy = []

    board_id = _create_id(abbr="B", options=options)
    root_item = _create_item(
        id=board_id, board_id=board_id, name=event_root["name"], abbr="B"
    )

    items_in_hierarchy.append(root_item)

    _process_items(
        event_items=event_root["items"],
        response_items=items_in_hierarchy,
        board_id=board_id,
        options=options,
        root=root_item,
    )

    return items_in_hierarchy
