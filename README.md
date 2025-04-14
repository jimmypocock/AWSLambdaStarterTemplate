# AWS Lambda Function Template

A professional template for AWS Lambda functions with development and production environments, testing framework, and local development capabilities.

## Features

- Multiple Lambda functions with separate endpoints
- Development and Production environments
- Testing framework with pytest and moto
- Local development and testing capabilities
- SAM template for deployment
- API Gateway integration
- Shared utilities for common functionality
- Cognito User Pool authentication for protected endpoints
- DynamoDB integration for item storage and retrieval

## Prerequisites

- Python 3.12 or later
- AWS SAM CLI
- AWS CLI configured with appropriate credentials
- Docker (for local testing)

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Local Development

To run the functions locally:
```bash
sam local start-api
```

The API will be available at:
- http://localhost:3000/hello (public endpoint)
- http://localhost:3000/goodbye (protected endpoint)

## Authentication with Cognito

The `/goodbye` endpoint is protected with Cognito authentication. Here's how to use it:

### 1. Deploy the Stack

First, deploy the stack to create the Cognito User Pool and API Gateway:
```bash
sam build && sam deploy --guided
```

After deployment, note down the following values from the stack outputs:
- UserPoolId
- UserPoolClientId
- ApiEndpoint

### 2. Create a User

Create a user in the Cognito User Pool using the AWS CLI:
```bash
aws cognito-idp admin-create-user \
    --user-pool-id <UserPoolId> \
    --username <desired_username> \
    --user-attributes Name=email,Value=<user_email> \
    --temporary-password <temporary_password> \
    --message-action SUPPRESS
```

### 3. Set User Password

Set the user's permanent password:
```bash
aws cognito-idp admin-set-user-password \
    --user-pool-id <UserPoolId> \
    --username <username> \
    --password <new_password> \
    --permanent
```

### 4. Authenticate and Get Token

Get an authentication token:
```bash
aws cognito-idp initiate-auth \
    --client-id <UserPoolClientId> \
    --auth-flow USER_PASSWORD_AUTH \
    --auth-parameters USERNAME=<username>,PASSWORD=<password>
```

The response will include an `IdToken`. Use this token in the Authorization header when calling the protected endpoint.

### 5. Call the Protected Endpoint

Make an authenticated request to the `/goodbye` endpoint:
```bash
curl -X GET \
  "$API_ENDPOINT/goodbye" \
  -H "Authorization: Bearer $TOKEN"
```

The response will include a personalized message with your user information:
```json
{
  "message": "Goodbye, <username>! (Environment: <environment>)",
  "user": {
    "username": "<username>",
    "email": "<email>"
  }
}
```

### 6. Configure Request Validation

For the Cognito authorizer to work properly, you need to configure request validation on the `/goodbye` endpoint's method request:

1. Go to the AWS Console and navigate to API Gateway
2. Select your API (it will be named something like `LambdaTemplate-<stack-id>`)
3. Click on the `/goodbye` resource
4. Click on the `GET` method
5. Click on "Method Request"
6. Under "Request Validator", select "Validate body, query string parameters, and headers"
7. Click the checkmark to save

This ensures that the request validation is properly configured for the Cognito authorizer to work.

## Lambda Layers and Local Testing

When testing Lambda functions with layers locally, SAM CLI automatically handles the layer content by downloading and mounting it to the correct path. You can test your functions with layers using:

```bash
# Invoke a specific function with an event file
sam local invoke HelloWorldFunction -e events/event.json

# Or invoke the GoodbyeWorld function
sam local invoke GoodbyeWorldFunction -e events/event.json
```

The layers will be automatically mounted to `/opt` in the Lambda runtime environment, just as they would be in production. You can access layer content in your code using the same paths as in production.

## Testing

Run the test suite:
```bash
pytest tests/
```

Run tests with coverage:
```bash
pytest --cov=src tests/
```

## Deployment

1. Build the application:
```bash
sam build
```

2. Deploy to development environment:
```bash
sam deploy --guided --parameter-overrides Environment=dev
```

3. Deploy to production environment:
```bash
sam deploy --guided --parameter-overrides Environment=prod
```

## Project Structure

```
LambdaTemplate/
├── src/
│   ├── functions/
│   │   ├── hello/
│   │   │   ├── __init__.py
│   │   │   └── app.py        # Hello World Lambda function
│   │   ├── goodbye/
│   │   │   ├── __init__.py
│   │   │   └── app.py        # Goodbye World Lambda function (protected)
│   │   ├── hello_item/
│   │   │   ├── __init__.py
│   │   │   └── app.py        # Hello Item Lambda function (DynamoDB)
│   │   └── __init__.py
│   ├── shared/
│   │   ├── __init__.py
│   │   └── utils.py          # Shared utilities
│   └── __init__.py
├── tests/
│   └── test_app.py           # Test suite
├── template.yaml             # SAM template
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Environment Variables

The functions use the following environment variables:
- `ENVIRONMENT`: Set to either 'dev' or 'prod' based on deployment
- `ITEMS_TABLE`: Name of the DynamoDB table (automatically set during deployment)

The environment variable is automatically set during deployment based on the `Environment` parameter:
```bash
# Sets ENVIRONMENT=prod in all Lambda functions
sam deploy --guided --parameter-overrides Environment=prod

# Sets ENVIRONMENT=dev in all Lambda functions
sam deploy --guided --parameter-overrides Environment=dev
```

You can verify the environment in the API response, which will include the current environment in the message.

## Adding New Functions

To add a new Lambda function:

1. Create a new directory under `src/functions/`
2. Create an `app.py` file with your Lambda handler
3. Add a new function resource in `template.yaml` with its API Gateway endpoint

## Testing the API Endpoints

### Using AWS CLI

1. First, get the API endpoint URL from your deployed stack:
```bash
aws cloudformation describe-stacks --stack-name LambdaTemplate --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' --output text
```

2. Test the endpoints using AWS CLI (replace YOUR_API_ENDPOINT with the actual endpoint URL):

```bash
# Test the /hello endpoint
aws apigateway test-invoke-method \
    --rest-api-id $(echo YOUR_API_ENDPOINT | cut -d/ -f3) \
    --resource-id /hello \
    --http-method GET \
    --path-with-query-string /hello

# Test the /goodbye endpoint (requires authentication)
aws apigateway test-invoke-method \
    --rest-api-id $(echo YOUR_API_ENDPOINT | cut -d/ -f3) \
    --resource-id /goodbye \
    --http-method GET \
    --path-with-query-string /goodbye \
    --headers 'Authorization=Bearer <IdToken>'
```

Note: These commands require:
- AWS CLI configured with valid credentials
- Appropriate IAM permissions to invoke the API endpoints
- For the /goodbye endpoint, a valid Cognito authentication token

## Deleting all resources

To delete all resources created by this template:
```bash
aws cloudformation delete-stack --stack-name LambdaTemplate
```

## License

MIT

## DynamoDB Integration

The template includes a DynamoDB table for storing items with the following configuration:
- Table Name: `{stack-name}-items`
- Partition Key: `itemId` (String)
- Billing Mode: PAY_PER_REQUEST

### New Endpoint: /hello/{itemId}

A new endpoint has been added that retrieves items from DynamoDB:
- Path: `/hello/{itemId}`
- Method: GET
- Description: Returns "Hello, {name}" where name is retrieved from the DynamoDB item

Example response:
```json
{
    "message": "Hello, John! (Environment: dev)"
}
```

If the item is not found, it returns a 404 error:
```json
{
    "message": "Item with ID 123 not found"
}
```