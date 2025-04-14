import os
import boto3
from common_utils import create_response, get_environment, log_event

def lambda_handler(event, context):
    """
    Lambda function that returns a hello message with the name from DynamoDB.

    Args:
        event (dict): API Gateway event
        context (object): Lambda context

    Returns:
        dict: Response containing status code and message
    """
    log_event(event, context)
    environment = get_environment(event)

    # Initialize DynamoDB client with environment variables
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['ITEMS_TABLE'])

    # Get itemId from path parameters
    item_id = event['pathParameters']['itemId']

    try:
        # Query DynamoDB for the item
        response = table.get_item(
            Key={
                'itemId': item_id
            }
        )

        # Check if item exists
        if 'Item' not in response:
            return create_response(
                status_code=404,
                body={
                    'message': f'Item with ID {item_id} not found'
                }
            )

        # Get the name from the item
        name = response['Item'].get('name', 'Unknown')

        return create_response(
            status_code=200,
            body={
                'message': f'Hello, {name}! (Environment: {environment})'
            }
        )

    except Exception as e:
        return create_response(
            status_code=500,
            body={
                'message': f'Error retrieving item: {str(e)}'
            }
        )