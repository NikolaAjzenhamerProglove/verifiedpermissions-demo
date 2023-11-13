from typing import Any, Optional

_REVERSE_MAP = {
    "BOARD": "B",
    "LIST": "L",
    "TASK": "T",
}


class DynamoDb:
    dynamodb_table: Any

    def __init__(self, dynamodb_table: Any) -> None:
        self.dynamodb_table = dynamodb_table

    def get_item_count(self) -> dict[str, int]:
        item_count: dict[str, int] = {
            "B": 0,
            "L": 0,
            "T": 0,
        }

        last_evaluated_key: Optional[dict] = None

        while True:
            params = {}

            if last_evaluated_key:
                params["ExclusiveStartKey"] = last_evaluated_key

            response = self.dynamodb_table.scan(**params)
            for item in response.get("Items", []):
                item_count[_REVERSE_MAP[item["type"]]] += 1

            last_evaluated_key = response.get("LastEvaluatedKey")

            if not last_evaluated_key:
                break

        return item_count
