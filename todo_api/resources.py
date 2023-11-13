from typing import Any


class Resources:
    dynamodb_table: Any
    verifiedpermissions: Any

    def __init__(self, dynamodb_table: Any, verifiedpermissions: Any) -> None:
        self.dynamodb_table = dynamodb_table
        self.verifiedpermissions = verifiedpermissions
