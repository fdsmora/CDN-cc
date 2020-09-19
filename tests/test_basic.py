import pytest
from app import create_app

def test_hello(client):
    response = client.get("/hello/")
    with open("dump.txt", "w") as f:
        f.write(response.data.decode('utf-8'))
    assert response.data == b"Hello, World!"
