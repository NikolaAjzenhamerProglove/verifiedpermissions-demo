from typing import Any


class Boto3Resources:
    dynamodb_table: Any
    verifiedpermissions: Any
    POLICY_STORE_ID: str
    PERMISSIONS_ENABLED: bool

    def __init__(
        self,
        dynamodb_table: Any,
        verifiedpermissions: Any,
        POLICY_STORE_ID: str,
        PERMISSIONS_ENABLED: bool,
    ) -> None:
        self.dynamodb_table = dynamodb_table
        self.verifiedpermissions = verifiedpermissions
        self.POLICY_STORE_ID = POLICY_STORE_ID
        self.PERMISSIONS_ENABLED = PERMISSIONS_ENABLED
