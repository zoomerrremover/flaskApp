import pytest
from src.app import app as application


@pytest.fixture()
def app():
    return application
