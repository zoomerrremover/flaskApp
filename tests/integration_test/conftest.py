import pytest
import os
import faker
from tests.common import down_docker_compose, start_docker_compose


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def user_generator():
    """
    Fixture that provides a generator yielding realistic user dictionaries.
    """

    def _generate_users(num_users=3):
        for _ in range(num_users):
            yield {
                "username": fake.user_name(),
                "password": fake.password(
                    length=12,
                    special_chars=True,
                    digits=True,
                    upper_case=True,
                    lower_case=True,
                ),
                "email": fake.email(),
            }

    return _generate_users
