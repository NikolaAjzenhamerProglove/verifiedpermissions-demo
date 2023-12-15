#!/bin/sh

# Cleanup
rm -rf .aws-sam

# Build
sam build

# Deploy
sam deploy

# Prepare data for the demo
sam remote invoke TodoAPIFunction --event-file=./events/todo_api/create_items_simple_board.json
sam remote invoke TodoAPIFunction --event-file=./events/todo_api/create_items_complex_board.json

# Save the test events to Lambda console
sam remote test-event put TodoCreateHierarchyFunction --name=SimpleHierarchy  --file=./events/todo_create_hierarchy/simple_board.json
sam remote test-event put TodoCreateHierarchyFunction --name=ComplexHierarchy --file=./events/todo_create_hierarchy/complex_board.json
