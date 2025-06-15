import pytest
import os
from faker import Faker  # Import Faker class
from tests.common import down_docker_compose, start_docker_compose
from src import app, Base, engine
from http import HTTPStatus
import jwt


@pytest.fixture()
def client(app):
    Base.metadata.create_all(engine)
    return app.test_client()


@pytest.fixture
def generate_users():
    def _generate_users(num_users=3):
        pre_existing_emails = [
            "carmena@comcast.net",
            "heine@sbcglobal.net",
            "madanm@yahoo.ca",
            "ryanshaw@att.net",
            "jugalator@verizon.net",
            "dmath@mac.com",
            "jimxugle@live.com",
            "gward@att.net",
            "bigmauler@yahoo.com",
            "vsprintf@outlook.com",
            "neuffer@yahoo.ca",
            "sacraver@gmail.com",
        ]
        fake = Faker()  # Initialize a Faker instance
        for _ in range(num_users):
            yield {
                "username": fake.user_name(),  # Corrected call
                "password": fake.password(
                    length=12,
                    special_chars=True,
                    digits=True,
                    upper_case=True,
                    lower_case=True,
                ),
                "email": fake.random_element(elements=pre_existing_emails),
            }

    return _generate_users


@pytest.fixture()
def registered_user_and_token(client, generate_users):
    user_data = next(generate_users())
    registration_response = client.post("/registration/", json=user_data)
    assert registration_response.status_code == HTTPStatus.OK
    access_token = registration_response.json["access_token"]

    return access_token, user_data
