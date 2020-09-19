import pytest
from project import create_app

def test_hello(client):
    response = client.get("/hello")
    print("RESPONSE:{}".format(response))
    assert response.data == b"Hello, World!"
