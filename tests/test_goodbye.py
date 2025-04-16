import json
import subprocess
import pytest

def test_goodbye():
    # Invoke the function using SAM CLI
    result = subprocess.run(
        ['sam', 'local', 'invoke', 'GoodbyeWorldFunction', '-e', 'events/goodbye_event.json'],
        capture_output=True,
        text=True
    )

    # Parse the response (body is already a JSON string)
    response = json.loads(result.stdout)
    body = json.loads(response['body'])

    # Assert the response
    assert response['statusCode'] == 200
    assert 'Goodbye' in body['message']
    assert body['user']['username'] == 'testuser'