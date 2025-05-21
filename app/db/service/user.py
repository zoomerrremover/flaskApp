from app.db.models.concrete import User
from email_validator import validate_email, EmailNotValidError
from flask import Response
from app.security.hash import passwd_to_hash, verify_password
from app.exceptions import InvalidDataError, ConflictingDataError
from app.constants import ErrorsMsgEnum
from app.exceptions import AuthenticationError
from app.constants import UserRolesEnum


def is_valid_email(email: str):
    validate_email(email, check_deliverability=True)


def create_user(username: str, password: str, email: str, role: UserRolesEnum = UserRolesEnum.user) -> User:
    return User(username=username, password=passwd_to_hash(password), email=email, role=role).save()


def get_user_by_id(user_id: int) -> User:
    data = User.get_by_id(user_id)
    print(data)
    return data


def get_user_login(username: str, password: str) -> User:
    user = User.get_user_by_name(username)
    if user and verify_password(password, user.password):
        return user
    else:
        raise AuthenticationError(ErrorsMsgEnum.ERR_AUTH)


def get_username_is_original(username: str) -> bool:
    user = User.get_user_by_name(username)
    if user:
        raise InvalidDataError(ErrorsMsgEnum.ERR_USERNAME_ORIGINAL)
    return True


def get_email_is_valid(email: str) -> bool:
    user = User.get_user_by_email(email)
    if user:
        raise ConflictingDataError(ErrorsMsgEnum.ERR_EMAIL_IS_ORIGINAL)
    is_valid_email(email)
    return True


def update_user_by_id(user_id: int, **kwargs):
    user = User.get_by_id(user_id)
    if kwargs.__contains__('email') and kwargs['email'] != user.email:
        is_valid_email(kwargs['email'])
    if kwargs.__contains__('username') and kwargs['username'] != user.username:
        get_username_is_original(kwargs['username'])
    if kwargs.__contains__('password') and not verify_password(kwargs['password'], user.password):
        kwargs['password'] = passwd_to_hash(kwargs['password'])
    return User.update_by_id(user_id, **kwargs)


def delete_user_by_id(user_id: int) -> None:
    return User.delete_by_id(user_id)
