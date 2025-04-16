#!/bin/bash

# Configuration
STACK_NAME="HelloWorld"

# Delete API stack first (depends on database and network)
echo "Deleting API stack..."
aws cloudformation delete-stack --stack-name ${STACK_NAME}-api
aws cloudformation wait stack-delete-complete --stack-name ${STACK_NAME}-api

# Delete database stack (depends on network)
echo "Deleting database stack..."
aws cloudformation delete-stack --stack-name ${STACK_NAME}-database
aws cloudformation wait stack-delete-complete --stack-name ${STACK_NAME}-database

# Delete network stack last (no dependencies)
echo "Deleting network stack..."
aws cloudformation delete-stack --stack-name ${STACK_NAME}-network
aws cloudformation wait stack-delete-complete --stack-name ${STACK_NAME}-network

echo "Cleanup complete!"