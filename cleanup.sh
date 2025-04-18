#!/bin/bash

# Configuration
STACK_NAME="HelloWorld"

# Delete API stack first (depends on database and network)
echo "Deleting API stack..."
sam delete --stack-name ${STACK_NAME}-api --no-prompts

# Delete database stack (depends on network)
echo "Deleting database stack..."
sam delete --stack-name ${STACK_NAME}-database --no-prompts

# Delete network stack last (no dependencies)
echo "Deleting network stack..."
sam delete --stack-name ${STACK_NAME}-network --no-prompts

echo "Cleanup complete!"