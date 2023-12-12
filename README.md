# verifiedpermissions-demo

A sample todo-list app for demoing _Amazon Verified Permissions_ service.

## Build & deploy

Building project is done by running the following command:

```bash
sam build
```

Deploying project is done by running the following command:

```bash
sam deploy --region=eu-west-1
```

## Cleanup

Removing the stack is done by running the following command:

```bash
aws cloudformation delete-stack --stack-name=verifiedpermissions-demo
```
