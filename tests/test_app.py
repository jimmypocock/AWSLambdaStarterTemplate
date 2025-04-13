import os
import json
from moto import mock_aws
import pytest
from src.app import lambda_handler

@pytest.fixture
def lambda_context():
    class LambdaContext:
        def __init__(self):
            self.function_name = "test-function"
            self.memory_limit_in_mb = 128
            self.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test-function"
            self.aws_request_id = "test-request-id"
    return LambdaContext()

def test_lambda_handler(lambda_context):
    # Test event
    event = {
        'httpMethod': 'GET',
        'path': '/hello'
    }
    
    # Set environment variable
    os.environ['ENVIRONMENT'] = 'test'
    
    # Call the function
    response = lambda_handler(event, lambda_context)
    
    # Parse the response
    response_body = json.loads(response['body'])
    
    # Assertions
    assert response['statusCode'] == 200
    assert response['headers']['Content-Type'] == 'application/json'
    assert response_body['message'] == 'Hello, World! (Environment: test)' 