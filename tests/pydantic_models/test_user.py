from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.constants import ErrorsMsgEnum
from src.exceptions import InvalidDataError
from src.models import (UserAdminGetModel, UserEmailModel, UserGetModel,
                        UserLogInModel, UserPasswordModel, UserRoleModel,
                        UserRoleUpdateModel, UserUpdateModel,
                        UserUsernameModel)

# Tests for UserUsernameModel


valid_username_data = {"username": "test_user123"}


valid_role_data = {"role": "user"}


valid_password_data = {"password": "StrongPass123!"}


valid_email_data = {"email": "test@example.com"}


base_user_get_data = {"id": 1, "date_registered": datetime.now(timezone.utc)}
base_user_get_data.update(valid_username_data)
base_user_get_data.update(valid_role_data)


base_user_admin_get_data = base_user_get_data.copy()
base_user_get_data.update(valid_email_data)


base_user_login_data = valid_username_data.copy()
base_user_login_data.update(valid_password_data)


base_user_role_update_data = {"id": 5}
base_user_role_update_data.update(valid_role_data)


base_user_update_data = valid_username_data.copy()
base_user_update_data.update(valid_password_data)
base_user_update_data.update(valid_email_data)


def test_user_username_model_valid(valid_username_data):
    user_username = UserUsernameModel(**valid_username_data)
    assert user_username.username == "test_user123"


def test_user_username_model_too_long(valid_username_data):
    invalid_data = valid_username_data.copy()
    invalid_data["username"] = "a" * 25  # Exceeds max_length
    with pytest.raises(ValidationError) as exc_info:
        UserUsernameModel(**invalid_data)
    assert "username" in str(exc_info.value)


def test_user_username_model_invalid_format(valid_username_data):
    invalid_data = valid_username_data.copy()
    invalid_data["username"] = "user name with space"  # Invalid by RE_USERNAME
    with pytest.raises(InvalidDataError) as exc_info:
        UserUsernameModel(**invalid_data)
    assert ErrorsMsgEnum.ERROR_USERNAME_INVALID in str(exc_info.value)


# Tests for UserRoleModel


def test_user_role_model_valid(valid_role_data):
    user_role = UserRoleModel(**valid_role_data)
    assert user_role.role == "user"


def test_user_role_model_too_long(valid_role_data):
    invalid_data = valid_role_data.copy()
    invalid_data["role"] = "a" * 11  # Exceeds max_length
    with pytest.raises(ValidationError) as exc_info:
        UserRoleModel(**invalid_data)
    assert "role" in str(exc_info.value)


def test_user_role_model_invalid_value(valid_role_data):
    invalid_data = valid_role_data.copy()
    invalid_data["role"] = "guest"  # Not in UserRolesEnum
    with pytest.raises(InvalidDataError) as exc_info:
        UserRoleModel(**invalid_data)
    assert ErrorsMsgEnum.ERROR_ROLE_INVALID in str(exc_info.value)


# Tests for UserPasswordModel


def test_user_password_model_valid(valid_password_data):
    user_password = UserPasswordModel(**valid_password_data)
    assert user_password.password == "StrongPass123!"


def test_user_password_model_too_long(valid_password_data):
    invalid_data = valid_password_data.copy()
    invalid_data["password"] = "a" * 33  # Exceeds max_length
    with pytest.raises(ValidationError) as exc_info:
        UserPasswordModel(**invalid_data)
    assert "password" in str(exc_info.value)


def test_user_password_model_invalid_format(valid_password_data):
    invalid_data = valid_password_data.copy()
    invalid_data["password"] = "weak"  # No digit
    with pytest.raises(InvalidDataError) as exc_info:
        UserPasswordModel(**invalid_data)
    assert ErrorsMsgEnum.ERROR_PASSWORD_WEAK in str(exc_info.value)


# Tests for UserEmailModel


def test_user_email_model_valid(valid_email_data):
    user_email = UserEmailModel(**valid_email_data)
    assert user_email.email == "test@example.com"


def test_user_email_model_invalid_format(valid_email_data):
    invalid_data = valid_email_data.copy()
    invalid_data["email"] = "invalid-email"  # Not a valid email
    with pytest.raises(ValidationError) as exc_info:
        UserEmailModel(**invalid_data)
    assert "email" in str(exc_info.value)


# Tests for UserGetModel


def test_user_get_model_valid(base_user_get_data):
    user_get = UserGetModel(**base_user_get_data)
    assert user_get.id == 1
    assert user_get.username == "test_user123"
    assert user_get.role == "user"
    assert isinstance(user_get.date_registered, datetime)


def test_user_get_model_invalid_id(base_user_get_data):
    invalid_data = base_user_get_data.copy()
    invalid_data["id"] = "not_an_int"
    with pytest.raises(ValidationError) as exc_info:
        UserGetModel(**invalid_data)
    assert "id" in str(exc_info.value)


def test_user_get_model_missing_required_field(base_user_get_data):
    invalid_data = base_user_get_data.copy()
    del invalid_data["username"]
    with pytest.raises(ValidationError) as exc_info:
        UserGetModel(**invalid_data)
    assert "username" in str(exc_info.value)


# Tests for UserAdminGetModel


def test_user_admin_get_model_valid(base_user_admin_get_data):
    user_admin_get = UserAdminGetModel(**base_user_admin_get_data)
    assert user_admin_get.id == 1
    assert user_admin_get.username == "test_user123"
    assert user_admin_get.role == "user"
    assert user_admin_get.email == "test@example.com"
    assert isinstance(user_admin_get.date_registered, datetime)


def test_user_admin_get_model_invalid_email(base_user_admin_get_data):
    invalid_data = base_user_admin_get_data.copy()
    invalid_data["email"] = "bad-email"
    with pytest.raises(ValidationError) as exc_info:
        UserAdminGetModel(**invalid_data)
    assert "email" in str(exc_info.value)


# Tests for UserLogInModel


def test_user_login_model_valid(base_user_login_data):
    user_login = UserLogInModel(**base_user_login_data)
    assert user_login.username == "test_user123"
    assert user_login.password == "StrongPass123!"


def test_user_login_model_invalid_username(base_user_login_data):
    invalid_data = base_user_login_data.copy()
    invalid_data["username"] = "us"  # Too short
    with pytest.raises(InvalidDataError) as exc_info:
        UserLogInModel(**invalid_data)
    assert ErrorsMsgEnum.ERROR_USERNAME_INVALID in str(exc_info.value)


def test_user_login_model_invalid_password(base_user_login_data):
    invalid_data = base_user_login_data.copy()
    invalid_data["password"] = "pass123"  # Too short / no uppercase
    with pytest.raises(InvalidDataError) as exc_info:
        UserLogInModel(**invalid_data)
    assert ErrorsMsgEnum.ERROR_PASSWORD_WEAK in str(exc_info.value)


# Tests for UserRoleUpdateModel


def test_user_role_update_model_valid(base_user_role_update_data):
    user_role_update = UserRoleUpdateModel(**base_user_role_update_data)
    assert user_role_update.id == 5
    assert user_role_update.role == "user"


def test_user_role_update_model_invalid_id(base_user_role_update_data):
    invalid_data = base_user_role_update_data.copy()
    invalid_data["id"] = "not_an_int"
    with pytest.raises(ValidationError) as exc_info:
        UserRoleUpdateModel(**invalid_data)
    assert "id" in str(exc_info.value)


def test_user_role_update_model_invalid_role(base_user_role_update_data):
    invalid_data = base_user_role_update_data.copy()
    invalid_data["role"] = "superadmin"  # Not a valid role
    with pytest.raises(InvalidDataError) as exc_info:
        UserRoleUpdateModel(**invalid_data)
    assert ErrorsMsgEnum.ERROR_ROLE_INVALID in str(exc_info.value)


# Tests for UserUpdateModel


def test_user_update_model_valid(base_user_update_data):
    user_update = UserUpdateModel(**base_user_update_data)
    assert user_update.username == "test_user123"
    assert user_update.password == "StrongPass123!"
    assert user_update.email == "test@example.com"


def test_user_update_model_invalid_username(base_user_update_data):
    invalid_data = base_user_update_data.copy()
    invalid_data["username"] = "u" * 25  # Too long
    with pytest.raises(ValidationError) as exc_info:
        UserUpdateModel(**invalid_data)
    assert "username" in str(exc_info.value)


def test_user_update_model_invalid_password(base_user_update_data):
    invalid_data = base_user_update_data.copy()
    invalid_data["password"] = "short"  # Invalid format
    with pytest.raises(InvalidDataError) as exc_info:
        UserUpdateModel(**invalid_data)
    assert ErrorsMsgEnum.ERROR_PASSWORD_WEAK in str(exc_info.value)


def test_user_update_model_invalid_email(base_user_update_data):
    invalid_data = base_user_update_data.copy()
    invalid_data["email"] = "not-an-email"
    with pytest.raises(ValidationError) as exc_info:
        UserUpdateModel(**invalid_data)
    assert "email" in str(exc_info.value)
