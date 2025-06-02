import pytest
from src.db import Base, engine
from src.app import app as application
from tests.common import down_docker_compose, start_docker_compose


@pytest.fixture()
def app():
    start_docker_compose("docker-compose.yml")
    Base.metadata.create_all(engine)
    yield application
    down_docker_compose("docker-compose.yml")


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def user_data():
    """
    Pytest fixture that provides a dictionary with unique user credentials.
    """

    user = {
        "username": "testuser",
        "password": "SecurePassword123!",  # Consider a stronger, but consistent test password
        "email": "test@gmail.com",
    }
    return user
