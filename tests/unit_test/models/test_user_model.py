import pytest
from datetime import datetime
from pydantic import ValidationError
from src.models import (
    UserAdminGetModel,
    UserEmailModel,
    UserGetModel,
    UserLogInModel,
    UserPasswordModel,
    UserRoleModel,
    UserRoleUpdateModel,
    UserUpdateModel,
    UserUsernameModel,
)
from src.exceptions import InvalidDataError
from src.constants import ErrorsMsgEnum


# Tests for UserUsernameModel
def test_user_username_model_valid(valid_username_data):
    user_username = UserUsernameModel(**valid_username_data)
    assert user_username.username == "test_user123"


def test_user_username_model_too_long(valid_username_data):
    valid_username_data["username"] = "a" * 25  # Exceeds max_length
    with pytest.raises(ValidationError) as exc_info:
        UserUsernameModel(**valid_username_data)
    assert "username" in str(exc_info.value)


def test_user_username_model_invalid_format(valid_username_data):
    valid_username_data["username"] = "user name with space"  # Invalid by RE_USERNAME
    with pytest.raises(InvalidDataError) as exc_info:
        UserUsernameModel(**valid_username_data)
    assert ErrorsMsgEnum.ERROR_USERNAME_INVALID in str(exc_info.value)


# Tests for UserRoleModel
def test_user_role_model_valid(valid_role_data):
    user_role = UserRoleModel(**valid_role_data)
    assert user_role.role == "user"


def test_user_role_model_too_long(valid_role_data):
    valid_role_data["role"] = "a" * 11  # Exceeds max_length
    with pytest.raises(ValidationError) as exc_info:
        UserRoleModel(**valid_role_data)
    assert "role" in str(exc_info.value)


def test_user_role_model_invalid_value(valid_role_data):
    valid_role_data["role"] = "guest"  # Not in UserRolesEnum
    with pytest.raises(InvalidDataError) as exc_info:
        UserRoleModel(**valid_role_data)
    assert ErrorsMsgEnum.ERROR_ROLE_INVALID in str(exc_info.value)


# Tests for UserPasswordModel
def test_user_password_model_valid(valid_password_data):
    user_password = UserPasswordModel(**valid_password_data)
    assert user_password.password == "StrongPass123!"


def test_user_password_model_too_long(valid_password_data):
    valid_password_data["password"] = "a" * 33  # Exceeds max_length
    with pytest.raises(ValidationError) as exc_info:
        UserPasswordModel(**valid_password_data)
    assert "password" in str(exc_info.value)


def test_user_password_model_invalid_format(valid_password_data):
    valid_password_data["password"] = "weak"  # No digit
    with pytest.raises(InvalidDataError) as exc_info:
        UserPasswordModel(**valid_password_data)
    assert ErrorsMsgEnum.ERROR_PASSWORD_WEAK in str(exc_info.value)


# Tests for UserEmailModel
def test_user_email_model_valid(valid_email_data):
    user_email = UserEmailModel(**valid_email_data)
    assert user_email.email == "test@example.com"


def test_user_email_model_invalid_format(valid_email_data):
    valid_email_data["email"] = "invalid-email"  # Not a valid email
    with pytest.raises(ValidationError) as exc_info:
        UserEmailModel(**valid_email_data)
    assert "email" in str(exc_info.value)


# Tests for UserGetModel
def test_user_get_model_valid(base_user_get_data):
    user_get = UserGetModel(**base_user_get_data)
    assert user_get.id == 1
    assert user_get.username == "test_user123"
    assert user_get.role == "user"
    assert isinstance(user_get.date_registered, datetime)


def test_user_get_model_invalid_id(base_user_get_data):
    base_user_get_data["id"] = "not_an_int"
    with pytest.raises(ValidationError) as exc_info:
        UserGetModel(**base_user_get_data)
    assert "id" in str(exc_info.value)


def test_user_get_model_missing_required_field(base_user_get_data):
    del base_user_get_data["username"]
    with pytest.raises(ValidationError) as exc_info:
        UserGetModel(**base_user_get_data)
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
    base_user_admin_get_data["email"] = "bad-email"
    with pytest.raises(ValidationError) as exc_info:
        UserAdminGetModel(**base_user_admin_get_data)
    assert "email" in str(exc_info.value)


# Tests for UserLogInModel
def test_user_login_model_valid(base_user_login_data):
    user_login = UserLogInModel(**base_user_login_data)
    assert user_login.username == "test_user123"
    assert user_login.password == "StrongPass123!"


def test_user_login_model_invalid_username(base_user_login_data):
    base_user_login_data["username"] = "us"  # Too short
    with pytest.raises(InvalidDataError) as exc_info:
        UserLogInModel(**base_user_login_data)
    assert ErrorsMsgEnum.ERROR_USERNAME_INVALID in str(exc_info.value)


def test_user_login_model_invalid_password(base_user_login_data):
    base_user_login_data["password"] = "pass123"  # Too short / no uppercase
    with pytest.raises(InvalidDataError) as exc_info:
        UserLogInModel(**base_user_login_data)
    assert ErrorsMsgEnum.ERROR_PASSWORD_WEAK in str(exc_info.value)


# Tests for UserRoleUpdateModel
def test_user_role_update_model_valid(base_user_role_update_data):
    user_role_update = UserRoleUpdateModel(**base_user_role_update_data)
    assert user_role_update.id == 5
    assert user_role_update.role == "user"


def test_user_role_update_model_invalid_id(base_user_role_update_data):
    base_user_role_update_data["id"] = "not_an_int"
    with pytest.raises(ValidationError) as exc_info:
        UserRoleUpdateModel(**base_user_role_update_data)
    assert "id" in str(exc_info.value)


def test_user_role_update_model_invalid_role(base_user_role_update_data):
    base_user_role_update_data["role"] = "superadmin"  # Not a valid role
    with pytest.raises(InvalidDataError) as exc_info:
        UserRoleUpdateModel(**base_user_role_update_data)
    assert ErrorsMsgEnum.ERROR_ROLE_INVALID in str(exc_info.value)


# Tests for UserUpdateModel
def test_user_update_model_valid(base_user_update_data):
    user_update = UserUpdateModel(**base_user_update_data)
    assert user_update.username == "test_user123"
    assert user_update.password == "StrongPass123!"
    assert user_update.email == "test@example.com"


def test_user_update_model_invalid_username(base_user_update_data):
    base_user_update_data["username"] = "u" * 25  # Too long
    with pytest.raises(ValidationError) as exc_info:
        UserUpdateModel(**base_user_update_data)

    assert "username" in str(exc_info.value)


def test_user_update_model_invalid_password(base_user_update_data):
    base_user_update_data["password"] = "short"  # Invalid format
    with pytest.raises(InvalidDataError) as exc_info:
        UserUpdateModel(**base_user_update_data)
    assert ErrorsMsgEnum.ERROR_PASSWORD_WEAK in str(exc_info.value)


def test_user_update_model_invalid_email(base_user_update_data):
    base_user_update_data["email"] = "not-an-email"
    with pytest.raises(ValidationError) as exc_info:
        UserUpdateModel(**base_user_update_data)
    assert "email" in str(exc_info.value)
