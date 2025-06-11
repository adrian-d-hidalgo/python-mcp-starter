"""
End-to-end tests for the MCP server.
"""

import threading
import time

import pytest
import requests
from src.server import MCPServer

HTTP_OK = 200  # HTTP 200 OK status code


@pytest.fixture
def server():
    """Start the server in a separate thread for testing."""
    server = MCPServer()
    server_thread = threading.Thread(target=server.run, kwargs={"port": 8001})
    server_thread.daemon = True
    server_thread.start()
    # Give the server time to start
    time.sleep(1)
    yield server
    # Cleanup will happen automatically when the thread is daemon


def test_server_hello_endpoint(server):
    """Test the hello endpoint."""
    response = requests.post(
        "http://localhost:8001/chat",
        json={"message": "hello"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == HTTP_OK
    data = response.json()
    assert "Hello from MCP server!" in data["response"]


def test_server_echo_endpoint(server):
    """Test the echo endpoint."""
    test_message = "test message"
    response = requests.post(
        "http://localhost:8001/chat",
        json={"message": f"echo {test_message}"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == HTTP_OK
    data = response.json()
    assert test_message in data["response"]


def test_server_status_endpoint(server):
    """Test the status endpoint."""
    response = requests.post(
        "http://localhost:8001/chat",
        json={"message": "status"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == HTTP_OK
    data = response.json()
    assert "status" in data["response"]
    assert "running" in data["response"]
