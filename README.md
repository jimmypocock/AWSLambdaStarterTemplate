# AWS Lambda Function Template

A professional template for AWS Lambda functions with development and production environments, testing framework, and local development capabilities.

## Features

- Simple Hello World Lambda function
- Development and Production environments
- Testing framework with pytest and moto
- Local development and testing capabilities
- SAM template for deployment
- API Gateway integration

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

To run the function locally:
```bash
sam local start-api
```

The API will be available at http://localhost:3000/hello

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

Deploy to development environment:
```bash
sam deploy --guided --parameter-overrides Environment=dev
```

Deploy to production environment:
```bash
sam deploy --guided --parameter-overrides Environment=prod
```

## Project Structure

```
LambdaTemplate/
├── src/
│   └── app.py           # Lambda function code
├── tests/
│   └── test_app.py      # Test suite
├── template.yaml        # SAM template
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Environment Variables

The function uses the following environment variables:
- `ENVIRONMENT`: Set to either 'dev' or 'prod' based on deployment

## License

MIT 