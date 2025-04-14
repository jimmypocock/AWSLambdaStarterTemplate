import json
import subprocess
import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the layers/python directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'layers', 'python'))

from src.functions.hello_item.app import lambda_handler

def test_hello_item():
    # Create a temporary env.json file with environment variables
    env_vars = {
        "HelloItemFunction": {
            "ITEMS_TABLE": "HelloWorld-items"
        }
    }
    with open('env.json', 'w') as f:
        json.dump(env_vars, f)

    try:
        # Invoke the function using SAM CLI with the event file
        process = subprocess.run(
            ["sam", "local", "invoke", "HelloItemFunction", "-e", "events/hello_item_event.json", "--env-vars", "env.json"],
            capture_output=True,
            text=True
        )

        # Print error output for debugging
        if process.stderr:
            print("Error output:", process.stderr)
        if process.stdout:
            print("Standard output:", process.stdout)

        # Check if the command was successful
        assert process.returncode == 0, f"SAM CLI command failed with return code {process.returncode}"

        # Parse the response
        response = json.loads(process.stdout)
        body = json.loads(json.loads(response["body"]))

        # Assert the response
        assert response["statusCode"] == 200
        assert "Hello, Mrs. Doubtfire!" in body["message"]
    finally:
        # Clean up the temporary file
        if os.path.exists('env.json'):
            os.remove('env.json')

def test_hello_item_not_found():
    # Create a temporary env.json file with environment variables
    env_vars = {
        "HelloItemFunction": {
            "ITEMS_TABLE": "HelloWorld-items"
        }
    }
    with open('env.json', 'w') as f:
        json.dump(env_vars, f)

    try:
        # Invoke the function using SAM CLI with the event file
        process = subprocess.run(
            ["sam", "local", "invoke", "HelloItemFunction", "-e", "events/hello_item_not_found_event.json", "--env-vars", "env.json"],
            capture_output=True,
            text=True
        )

        # Print error output for debugging
        if process.stderr:
            print("Error output:", process.stderr)
        if process.stdout:
            print("Standard output:", process.stdout)

        # Check if the command was successful
        assert process.returncode == 0, f"SAM CLI command failed with return code {process.returncode}"

        # Parse the response
        response = json.loads(process.stdout)
        body = json.loads(json.loads(response["body"]))

        # Assert the response
        assert response["statusCode"] == 404
        assert "Item with ID nonexistent not found" in body["message"]
    finally:
        # Clean up the temporary file
        if os.path.exists('env.json'):
            os.remove('env.json')