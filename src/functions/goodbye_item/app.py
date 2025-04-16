import os
import psycopg2
from common_utils import create_response, get_environment, log_event

def get_db_connection():
    """
    Creates a connection to the RDS PostgreSQL database.
    """
    db_host = os.environ['DB_HOST']
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_port = os.environ['DB_PORT']

    return psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
        port=db_port
    )

def lambda_handler(event, context):
    """
    Lambda function that returns a goodbye message with the name from RDS.

    Args:
        event (dict): API Gateway event
        context (object): Lambda context

    Returns:
        dict: Response containing status code and message
    """
    log_event(event, context)
    environment = get_environment(event)

    # Get itemId from path parameters
    item_id = event['pathParameters']['itemId']

    try:
        # Connect to RDS
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query RDS for the item
        cursor.execute("SELECT name FROM items WHERE id = %s", (item_id,))
        result = cursor.fetchone()

        # Close database connection
        cursor.close()
        connection.close()

        # Check if item exists
        if not result:
            return create_response(
                status_code=404,
                body={
                    'message': f'Item with ID {item_id} not found'
                }
            )

        # Get the name from the result
        name = result[0]

        return create_response(
            status_code=200,
            body={
                'message': f'Goodbye, {name}! (Environment: {environment})'
            }
        )

    except Exception as e:
        return create_response(
            status_code=500,
            body={
                'message': f'Error retrieving item: {str(e)}'
            }
        )