import pytest
from datetime import datetime, timezone
from src.db import User

MOCK_JWT_KEY = "super_secret_test_key"
MOCK_ALGORITHM = "HS256"
MOCK_ACCESS_TOKEN_TIME = 15


@pytest.fixture
def real_user_instance():
    """Provides a real User model instance for testing."""
    return User(
        id=456,
        username="john_doe",
        role="user",
        date_registered=datetime(2023, 1, 1, 12, 0, 0),
        email="john.doe@example.com",
        password="hashed_password_123",
    )


@pytest.fixture
def fixed_datetime(mocker):
    """
    Mocks datetime.datetime.now() to return a fixed datetime for predictable tests.
    Also mocks time.time() to match the timestamp of the fixed datetime.
    """
    fixed_now = datetime.now(timezone.utc)  # Fixed date and time
    # mocker.patch("src.security.jwt_service.datetime.now", return_value=fixed_now)
    return fixed_now


@pytest.fixture
def mock_jwt_encode(mocker):
    """Mocks jwt.encode to return a predictable token string."""
    mock_encode = mocker.patch(
        "src.security.jwt_service.jwt.encode", return_value="mock_jwt_token_string"
    )
    return mock_encode


@pytest.fixture
def mock_jwt_decode(mocker):
    """Mocks jwt.decode to return a predictable payload dictionary."""
    mock_decode = mocker.patch(
        "jwt.decode",
        return_value={
            "user_id": 456,  # Matches real_user_instance.id
            "exp": (
                datetime(2023, 10, 26, 10, 15, 0)
            ).timestamp(),  # Matches fixed_datetime + 15 min
            "iat": (
                datetime(2023, 10, 26, 10, 0, 0)
            ).timestamp(),  # Matches fixed_datetime
        },
    )
    return mock_decode


@pytest.fixture(autouse=True)
def mock_settings_constants(mocker):
    """
    Mocks the global settings constants JWT_KEY, ALGORITHM, ACCESS_TOKEN_TIME
    to ensure tests are isolated from actual settings.
    `autouse=True` means this fixture runs for every test.
    """
    mocker.patch("src.security.jwt_service.JWT_KEY", "test_secret_key_from_fixture")
    mocker.patch("src.security.jwt_service.ALGORITHM", "HS256")
    mocker.patch("src.security.jwt_service.ACCESS_TOKEN_TIME", 15)
