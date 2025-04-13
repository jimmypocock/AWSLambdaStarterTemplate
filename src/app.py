import os
import json

def lambda_handler(event, context):
    """
    Lambda function that returns a simple Hello World message.
    
    Args:
        event (dict): API Gateway event
        context (object): Lambda context
    
    Returns:
        dict: Response containing status code and message
    """
    environment = os.environ.get('ENVIRONMENT', 'dev')
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Hello, World! (Environment: {environment})'
        }),
        'headers': {
            'Content-Type': 'application/json'
        }
    } 