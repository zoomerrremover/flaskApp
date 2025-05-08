from app.db.models import User
from email_validator import validate_email, EmailNotValidError
from flask import Response
from app.models.user import UserRead, UserSuRead
from app.security.hash import passwd_to_hash, verify_password
from app.exceptions import InvalidDataError, ConflictingDataError
from app.constants import Errors
from app.exceptions import AuthenticationError
from typing import List

def is_valid_email(email: str):
    validate_email(email, check_deliverability=True)


def create_user(username: str, password: str, email: str, role: str = 'user') -> User:
    return User(username=username, password=passwd_to_hash(password), email=email, role=role).save()


def get_all_users() -> List[UserRead]:
    users = User.get_users()
    return [UserRead(username=data.username, role=data.role) for data in users]


def get_users_by_name(username: str) -> List[UserRead]:
    users = User.get_users_by_username(username)
    return [UserRead(username=data.username, role=data.role) for data in users]


def get_users_by_role(role: str) -> List[UserRead]:
    users = User.get_users_by_role(role)
    return [UserRead(username=data.username, role=data.role) for data in users]


def get_su_users_by_email(email: str) -> List[UserSuRead]:
    users = User.get_users_by_email(email)
    return [UserSuRead(username=data.username, role=data.role, email=data.email) for data in users]


def get_user_by_id(user_id: int, admin: bool = False) -> User:
    data = User.get_user_by_id(user_id)
    return UserSuRead(username=data.username, email=data.email, role=data.role) if admin else\
        UserRead(username=data.username, role=data.role)


def get_user_login(username: str, password: str) -> User:
    user = User.get_user_by_exact_name(username)
    if user and verify_password(password, user.password):
        return user
    else:
        raise AuthenticationError(Errors.ERR_AUTH)


def get_username_is_original(username: str) -> bool:
    user = User.get_user_by_exact_name(username)
    if user:
        raise InvalidDataError(Errors.ERR_USERNAME_ORIGINAL)
    return True


def get_email_is_valid(email: str) -> bool:
    user = User.get_user_by_exact_email(email)
    if user:
        raise ConflictingDataError(Errors.ERR_EMAIL_IS_ORIGINAL)
    is_valid_email(email)
    return True


def update_user_by_id(user_id: int, **kwargs) -> int:
    if 'email' in kwargs:
        is_valid_email(kwargs['email'])
    if 'username' in kwargs:
        get_username_is_original(kwargs['username'])
    return User.update_user_by_id(user_id, **kwargs)


def delete_user_by_id(user_id: int) -> None:
    return User.delete_user_by_id(user_id)
