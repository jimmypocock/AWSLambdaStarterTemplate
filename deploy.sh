#!/bin/bash

# Exit on error
set -e

# Default values
ENVIRONMENT="dev"
STAGE="Dev"
STACK_NAME="HelloWorld"
DB_USERNAME=""
DB_PASSWORD=""
S3_BUCKET="aws-sam-cli-managed-default-samclisourcebucket-90pcpp7zo8bz"

# Function to check stack status and delete if in ROLLBACK_COMPLETE
check_and_delete_stack() {
    local stack_name=$1
    local status=$(aws cloudformation describe-stacks --stack-name $stack_name --query "Stacks[0].StackStatus" --output text 2>/dev/null || echo "NOT_FOUND")

    if [ "$status" == "ROLLBACK_COMPLETE" ]; then
        echo "Stack $stack_name is in ROLLBACK_COMPLETE state. Deleting before redeploying..."
        aws cloudformation delete-stack --stack-name $stack_name
        aws cloudformation wait stack-delete-complete --stack-name $stack_name
    fi
}

# Function to get stack output value
get_stack_output() {
    local stack_name=$1
    local output_key=$2
    aws cloudformation describe-stacks \
        --stack-name $stack_name \
        --query "Stacks[0].Outputs[?OutputKey=='$output_key'].OutputValue" \
        --output text
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --environment)
      ENVIRONMENT="$2"
      shift 2
      ;;
    --stage)
      STAGE="$2"
      shift 2
      ;;
    --stack-name)
      STACK_NAME="$2"
      shift 2
      ;;
    --db-username)
      DB_USERNAME="$2"
      shift 2
      ;;
    --db-password)
      DB_PASSWORD="$2"
      shift 2
      ;;
    --s3-bucket)
      S3_BUCKET="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required parameters
if [ -z "$DB_USERNAME" ]; then
  echo "Error: --db-username is required"
  exit 1
fi

if [ -z "$DB_PASSWORD" ]; then
  echo "Error: --db-password is required"
  exit 1
fi

echo "Deploying stacks with the following parameters:"
echo "Environment: $ENVIRONMENT"
echo "Stage: $STAGE"
echo "Stack Name: $STACK_NAME"

# Check and delete stacks in ROLLBACK_COMPLETE state
check_and_delete_stack "${STACK_NAME}-network"
check_and_delete_stack "${STACK_NAME}-database"
check_and_delete_stack "${STACK_NAME}-api"

# Deploy network stack
echo "Deploying network stack..."
sam deploy -t network.yaml \
  --stack-name "${STACK_NAME}-network" \
  --parameter-overrides \
    Environment="${ENVIRONMENT}" \
    Stage="${STAGE}" \
  --capabilities CAPABILITY_IAM \
  --no-fail-on-empty-changeset \
  --s3-bucket "${S3_BUCKET}"

# Get network stack outputs
VPC_ID=$(get_stack_output "${STACK_NAME}-network" "VPCId")
PRIVATE_SUBNET_1_ID=$(get_stack_output "${STACK_NAME}-network" "PrivateSubnet1Id")
PRIVATE_SUBNET_2_ID=$(get_stack_output "${STACK_NAME}-network" "PrivateSubnet2Id")

# Deploy database stack
echo "Deploying database stack..."
sam deploy -t database.yaml \
  --stack-name "${STACK_NAME}-database" \
  --parameter-overrides \
    Environment="${ENVIRONMENT}" \
    Stage="${STAGE}" \
    DBUsername="${DB_USERNAME}" \
    DBPassword="${DB_PASSWORD}" \
    NetworkStackName="${STACK_NAME}-network" \
    VpcId="${VPC_ID}" \
    PrivateSubnet1Id="${PRIVATE_SUBNET_1_ID}" \
    PrivateSubnet2Id="${PRIVATE_SUBNET_2_ID}" \
  --capabilities CAPABILITY_IAM \
  --no-fail-on-empty-changeset \
  --s3-bucket "${S3_BUCKET}"

# Deploy API stack
echo "Deploying API stack..."
sam deploy -t api.yaml \
  --stack-name "${STACK_NAME}-api" \
  --parameter-overrides \
    Environment="${ENVIRONMENT}" \
    Stage="${STAGE}" \
    NetworkStackName="${STACK_NAME}-network" \
    DatabaseStackName="${STACK_NAME}-database" \
    DBUsername="${DB_USERNAME}" \
    DBPassword="${DB_PASSWORD}" \
  --capabilities CAPABILITY_IAM \
  --no-fail-on-empty-changeset \
  --s3-bucket "${S3_BUCKET}"

echo "Deployment completed successfully!"