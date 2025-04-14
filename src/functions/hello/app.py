from common_utils import create_response, get_environment, log_event

def lambda_handler(event, context):
    """
    Lambda function that returns a hello message.

    Args:
        event (dict): API Gateway event
        context (object): Lambda context

    Returns:
        dict: Response containing status code and message
    """
    log_event(event, context)
    environment = get_environment(event)

    return create_response(
        status_code=200,
        body={
            'message': f'Hello, World! (Environment: {environment})'
        }
    )