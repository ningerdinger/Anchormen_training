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


def test_hello_world(client):
    answer = client.get("/")
    assert re.match(b".* on host .*", answer.data)
