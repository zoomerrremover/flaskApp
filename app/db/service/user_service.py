from app.db.models import User
from email_validator import validate_email, EmailNotValidError
from http import HTTPStatus
from flask import Response
from app.models.user import UserRead, UserSuRead
from app.security.hash import passwd_to_hash, verify_password
from app.common import str_compare
from builtins import AuthenticationError
from pydantic.main import ValidationError
from app.settings import ERR_AUTH, ERR_USERNAME_ORIGINAL

def is_valid_email(email:str):
    validate_email(email, check_deliverability=True)


def create_user(username: str, password: str, email: str, role: str = 'user') -> User:
    return User(username=username,
                password=passwd_to_hash(password),
                email=email,
                role=role
                ).save()


def get_users():
    users = User.get_users()
    return [UserRead(username=data.username) for data in users]


def get_users_by_name(username: str):
    users = User.get_users_by_username(username)
    return [UserRead(username=data.username) for data in users]


def get_user_by_id(user_id: int):
    data = User.get_user_by_id(user_id)
    return UserRead(username=data.username)


def get_user_login(username: str, password: str) -> User:
    user = User.get_user_by_exact_name(username)
    if user and verify_password(password, user.password):
        return user
    else:
        raise AuthenticationError(ERR_AUTH)


def get_username_is_original(username: str) -> bool:
    user = User.get_user_by_exact_name(username)
    if user:
        raise ValidationError(ERR_USERNAME_ORIGINAL)
    return True


def get_email_is_valid(email: str) -> bool:
    user = User.get_user_by_exact_email(email)
    if not user and is_valid_email(email):
        return True
    else:
        raise ValidationError(ERR_USERNAME_ORIGINAL)


def get_su_user_by_id(user_id: int) -> UserSuRead:
    data = User.get_user_by_id(user_id)
    return UserSuRead(username=data.username, email=data.email)


def delete_user_by_id(user_id: int):
    return User.delete_user_by_id(user_id)


def update_user_by_id(user_id: int, **kwargs):
    return User.update_user_by_id(user_id, **kwargs)
