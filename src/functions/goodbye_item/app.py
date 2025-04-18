import boto3
import os
from common_utils import create_response, get_environment, log_event

def lambda_handler(event, context):
    """
    Lambda function that returns a goodbye message for a user by ID using RDS Data API.

    Args:
        event (dict): API Gateway event
        context (object): Lambda context

    Returns:
        dict: Response containing status code and message
    """
    log_event(event, context)
    environment = get_environment(event)

    # Get user ID from path parameters
    id = event.get('pathParameters', {}).get('id')
    if not id:
        return create_response(
            status_code=400,
            body={'message': 'User ID is required'}
        )

    # Initialize RDS Data API client
    rds_data = boto3.client('rds-data')

    try:
        # Execute SQL statement using RDS Data API
        response = rds_data.execute_statement(
            resourceArn=os.environ['DB_CLUSTER_ARN'],
            secretArn=os.environ['DB_SECRET_ARN'],
            database=os.environ['DB_NAME'],
            sql='SELECT name FROM items WHERE id = :id',
            parameters=[
                {
                    'name': 'id',
                    'value': {'stringValue': id}
                }
            ]
        )

        # Check if user was found
        if not response.get('records'):
            return create_response(
                status_code=404,
                body={'message': f'Item with ID {id} not found'}
            )

        # Extract user data from response
        item = response['records'][0]
        name = item[0]['stringValue']

        return create_response(
            status_code=200,
            body={
                'message': f'Goodbye, {name}! (Environment: {environment})',
                'user': {
                    'id': id,
                    'name': name
                }
            }
        )

    except Exception as e:
        return create_response(
            status_code=500,
            body={'message': f'Error retrieving user: {str(e)}'}
        )