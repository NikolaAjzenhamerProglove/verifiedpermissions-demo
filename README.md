# verifiedpermissions-demo

A sample todo-list app for demoing _Amazon Verified Permissions_ service.

## Build & deploy

Building project is done by running the following command:

```bash
./tools/setup.sh
```

## Testing scenarios

### Scenario 1: Permissions are disabled

```bash
sam remote invoke TodoAPIFunction --event-file=./events/todo_api/get_item_permissions_off.json
```

### Scenario 2: Permissions are enabled; user has no permissions

```bash
sam remote invoke TodoAPIFunction --event-file=./events/todo_api/get_item_permissions_on_denied.json
```

### Scenario 3: Permissions are enabled; user has permissions

```bash
sam remote invoke TodoCreatePermissionFunction --event-file=./events/todo_create_permission/enable_alice_to_get_task3.json
sam remote invoke TodoAPIFunction --event-file=./events/todo_api/get_item_permissions_on_allowed.json
```

## Cleanup

Removing the stack is done by running the following command:

```bash
./tools/teardown.sh
```
