import pytest
from app import create_app

def test_hello(client):
    response = client.get("/hello/")
    assert response.data == b"Hello, World!"

