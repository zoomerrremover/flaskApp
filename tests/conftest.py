import pytest

from src import app as application


@pytest.fixture()
def app():
    return application


@pytest.fixture()
def mock_db_session(mocker):
    return mocker.patch("src.db.models.common.session", autospec=True)
