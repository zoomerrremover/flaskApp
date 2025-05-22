from app.db.models.concrete import User
from email_validator import validate_email, EmailNotValidError
from flask import Response
from app.security.hash import verify_password
from app.constants import ErrorsMsgEnum
from app.exceptions import AuthenticationError, InvalidDataError
from app.db.service.common import DbService


class UserDbService(DbService):
    MODEL = User

    @classmethod
    def is_valid_email(cls, email: str):
        try:
            validate_email(email, check_deliverability=True)
        except EmailNotValidError:
            raise InvalidDataError(ErrorsMsgEnum.ERR_EMAIL_VALID)

    @classmethod
    def get_user_login(cls, username: str, password: str) -> User:
        user = User.get_user_by_name(username)
        if user and verify_password(password, user.password):
            return user
        else:
            raise AuthenticationError(ErrorsMsgEnum.ERR_AUTH)
