from shared.utils import create_response, get_environment

def lambda_handler(event, context):
    """
    Lambda function that returns a goodbye message.

    Args:
        event (dict): API Gateway event
        context (object): Lambda context

    Returns:
        dict: Response containing status code and message
    """
    environment = get_environment(event)

    return create_response(
        status_code=200,
        body={
            'message': f'Goodbye, World! (Environment: {environment})'
        }
    )