import pytest
from src import app as application


@pytest.fixture()
def app():
    return application
