#!/bin/bash

# Configuration
STACK_NAME="HelloWorld"

# Delete API stack first (depends on database and network)
echo "Deleting API stack..."
sam delete --stack-name ${STACK_NAME}-api --no-prompts

# Wait for API stack to be fully deleted
echo "Waiting for API stack to be deleted..."
aws cloudformation wait stack-delete-complete --stack-name ${STACK_NAME}-api

# Delete database stack (depends on network)
echo "Deleting database stack..."
sam delete --stack-name ${STACK_NAME}-database --no-prompts

# Wait for database stack to be fully deleted
echo "Waiting for database stack to be deleted..."
aws cloudformation wait stack-delete-complete --stack-name ${STACK_NAME}-database

# Delete network stack last (no dependencies)
echo "Deleting network stack..."
sam delete --stack-name ${STACK_NAME}-network --no-prompts

# Wait for network stack to be fully deleted
echo "Waiting for network stack to be deleted..."
aws cloudformation wait stack-delete-complete --stack-name ${STACK_NAME}-network

echo "Cleanup complete!"