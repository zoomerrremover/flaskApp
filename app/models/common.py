from pydantic.main import BaseModel, ValidationError
from pydantic import validator
from app.settings import RE_USERNAME,RE_PASSWORD, ERR_USERNAME, ERR_PASSWORD, ERR_ROLES, USER_ROLES
from flask import Response

class ValidationModel(BaseModel):
    @staticmethod
    def validate_username(value):
        if not RE_USERNAME.match(value):
            raise ValidationError(ERR_USERNAME)
        return value
    @staticmethod
    def validate_password(value):
        if not RE_PASSWORD.match(value):
            raise ValidationError(ERR_PASSWORD)
        return value
    @staticmethod
    def validate_role(value):
        if value not in USER_ROLES:
            raise ValidationError(ERR_ROLES)
        return value

