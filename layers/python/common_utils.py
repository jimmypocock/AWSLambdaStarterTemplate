import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def create_response(status_code: int, body: dict, headers: dict = None) -> dict:
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

def get_environment(event: dict) -> str:
    """
    Returns the current environment based on API Gateway stage.

    Args:
        event (dict): API Gateway event

    Returns:
        str: Environment name in lowercase
    """
    request_context = event.get('requestContext', {})
    stage = request_context.get('stage', 'Dev')
    return stage.lower()  # Convert to lowercase for consistency

def log_event(event: dict, context: object) -> None:
    """
    Log the incoming event and context information.

    Args:
        event (dict): Lambda event
        context (object): Lambda context
    """
    logger.info("Event: %s", json.dumps(event))
    logger.info("Context: %s", context)