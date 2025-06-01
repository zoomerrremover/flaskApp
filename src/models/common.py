from flask import Response
from pydantic.main import BaseModel
from pydantic import validator
from pydantic.fields import Field
from typing import Optional
from ..settings import RE_USERNAME, RE_PASSWORD, RE_TEXT_CONTENT
from ..constants import ErrorsMsgEnum, UserRolesEnum
from ..exceptions import InvalidDataError


class ValidationTextModel(BaseModel):

    @staticmethod
    def validate_text_content(value):
        if not RE_TEXT_CONTENT.match(value):
            raise InvalidDataError(ErrorsMsgEnum.ERR_TEXT_CONTENT)
        return value


class ValidationPasswordModel(BaseModel):

    @staticmethod
    def validate_password(value):
        if not RE_PASSWORD.match(value):
            raise InvalidDataError(ErrorsMsgEnum.ERR_PASSWORD)
        return value


class ValidationUserNameModel(BaseModel):

    @staticmethod
    def validate_username(value):
        if not RE_USERNAME.match(value):
            raise InvalidDataError(ErrorsMsgEnum.ERR_USERNAME_VALIDITY)
        return value


class ValidationRoleModel(BaseModel):

    @staticmethod
    def validate_role(value):
        try:
            UserRolesEnum(value)
        except ValueError:
            raise InvalidDataError(ErrorsMsgEnum.ERR_ROLES)


class GenericIdModel(BaseModel):
    id: int = Field()
    limit: Optional[int] = 20

    @validator("limit")
    def model_validate_limit(cls, value):
        if 0 > value or value < 100:
            raise InvalidDataError(ErrorsMsgEnum.ERR_LIMIT)


class StringSearchModel(BaseModel):
    search: str = Field(max_length=40)
    limit: Optional[int] = 20

    @validator("limit")
    def model_validate_limit(cls, value):
        if 0 > value or value < 100:
            raise InvalidDataError(ErrorsMsgEnum.ERR_LIMIT)
