"""Test objects used to test the behavior of endpoints in main.py.

Usage: test_main.py

Attributes:
    SECRET: A str constrant representing the encryption secret for JWTs used
        for the tests
    TOKEN: A str constant representing the JWT used for the tests
    EMAIL: A str constant representing the email used for the tests
    PASSWORD: A str constant representing the password used for the tests
"""

import json
import os

import pytest

from app import app

SECRET = "TestSecret"
EMAIL = "wolf@thedoor.com"
PASSWORD = "huff-puff"


@pytest.fixture(name="client")
def fixture_client():
    """Creates the test client as a pytest fixture.

    Yields:
        client: A flask Flask test_client object representing the client to
            run the tests with
    """
    os.environ["JWT_SECRET"] = SECRET
    app.config["TESTING"] = True
    client = app.test_client()

    yield client


def test_health(client):
    """Test successful health check.

    Args:
        client: A flask Flask test_client object representing the client to
            run the tests with
    """
    response = client.get("/")

    assert response.status_code == 200
    assert response.json == "Healthy"


def test_auth(client):
    """Test successful JWT creation.

    Args:
        client: A flask Flask test_client object representing the client to
            run the tests with
    """
    body = {"email": EMAIL, "password": PASSWORD}

    response = client.post(
        "/auth", data=json.dumps(body), content_type="application/json"
    )

    token = response.json["token"]

    assert response.status_code == 200
    assert token is not None


def test_contents(client):
    """Test successful retrieval of JWT contents.

    Args:
        client: A flask Flask test_client object representing the client to
            run the tests with
    """
    body = {"email": EMAIL, "password": PASSWORD}
    response = client.post(
        "/auth", data=json.dumps(body), content_type="application/json"
    )
    token = response.json["token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/contents", headers=headers)

    assert response.status_code == 200
    assert response.json.get("email") == EMAIL


if __name__ == "__main__":
    pytest.main()
