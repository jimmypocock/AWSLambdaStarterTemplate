import json
import os

def create_response(status_code, body, headers=None):
    """
    Creates a standardized API Gateway response.

    Args:
        status_code (int): HTTP status code
        body (dict): Response body
        headers (dict, optional): Additional headers

    Returns:
        dict: API Gateway response
    """
    default_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }

    if headers:
        default_headers.update(headers)

    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': default_headers
    }

def get_environment(event):
    """Returns the current environment based on API Gateway stage"""
    request_context = event.get('requestContext', {})
    stage = request_context.get('stage', 'Dev')
    return stage.lower()  # Convert to lowercase for consistency