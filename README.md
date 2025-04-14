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
- http://localhost:3000/hello
- http://localhost:3000/goodbye

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
│   │   │   └── app.py        # Goodbye World Lambda function
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

# Test the /goodbye endpoint
aws apigateway test-invoke-method \
    --rest-api-id $(echo YOUR_API_ENDPOINT | cut -d/ -f3) \
    --resource-id /goodbye \
    --http-method GET \
    --path-with-query-string /goodbye
```

Note: These commands require:
- AWS CLI configured with valid credentials
- Appropriate IAM permissions to invoke the API endpoints

## License

MIT