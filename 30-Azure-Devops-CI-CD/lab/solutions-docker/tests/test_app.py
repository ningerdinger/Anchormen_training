import re

import pytest

from app.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_square(client):
    answer = client.get("square_number?number=2")
    assert b"Square of 2.0 is 4.0" == answer.data


def test_square_string(client):
    answer = client.get("square_number?number=a")
    assert b"Not a numerical value" == answer.data


def test_square_empty(client):
    answer = client.get("square_number")
    assert b"Empty input" == answer.data


def test_hello_world(client):
    answer = client.get("/")
    assert re.match(b".* on host .*", answer.data)
