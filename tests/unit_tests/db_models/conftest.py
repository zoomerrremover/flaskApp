import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture()
def mock_db_session(mocker):
    return mocker.patch("src.db.models.common.session", autospec=True)
