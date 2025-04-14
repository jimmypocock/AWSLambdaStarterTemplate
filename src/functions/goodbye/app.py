import json
from common_utils import create_response, get_environment, log_event

def lambda_handler(event, context):
    """
    Lambda function that returns a goodbye message for authenticated users.

    Args:
        event (dict): API Gateway event
        context (object): Lambda context

    Returns:
        dict: Response containing status code and message
    """
    log_event(event, context)
    environment = get_environment(event)

    # Get the authenticated user's information from the request context
    request_context = event.get('requestContext', {})
    authorizer = request_context.get('authorizer', {})
    claims = authorizer.get('claims', {})

    # Extract user information
    username = claims.get('cognito:username', 'User')
    email = claims.get('email', '')

    return create_response(
        status_code=200,
        body=json.dumps({
            'message': f'Goodbye, {username}! (Environment: {environment})',
            'user': {
                'username': username,
                'email': email
            }
        })
    )