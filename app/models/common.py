from pydantic.main import BaseModel, ValidationError
from pydantic import validator
from app.settings import RE_USERNAME, RE_PASSWORD, RE_TEXT_CONTENT
from app.constants import Errors, UserRole
from flask import Response


class ValidationTextModel(BaseModel):

    @staticmethod
    def validate_text_content(value):
        if not RE_TEXT_CONTENT.match(value):
            raise ValidationError(Errors.ERR_TEXT_CONTENT)
        return value


class ValidationPasswordModel(BaseModel):

    @staticmethod
    def validate_password(value):
        if not RE_PASSWORD.match(value):
            raise ValidationError(Errors.ERR_PASSWORD)
        return value


class ValidationUserNameModel(BaseModel):

    @staticmethod
    def validate_username(value):
        if not RE_USERNAME.match(value):
            raise ValidationError(Errors.ERR_USERNAME_VALIDITY)
        return value


class ValidationRoleModel(BaseModel):

    @staticmethod
    def validate_role(value):
        return UserRole(value)
