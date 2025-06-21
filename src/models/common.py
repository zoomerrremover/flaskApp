from pydantic.main import BaseModel
from pydantic import field_validator
from pydantic.fields import Field
from typing import Optional
from src.settings import RE_USERNAME, RE_PASSWORD, RE_TEXT_CONTENT
from src.constants import ErrorsMsgEnum, UserRolesEnum
from src.exceptions import InvalidDataError


class ValidationTextModel(BaseModel):

    @staticmethod
    def validate_text_content(value):
        if not RE_TEXT_CONTENT.match(value):
            raise InvalidDataError(ErrorsMsgEnum.ERROR_TEXT_CONTENT)
        return value


class ValidationPasswordModel(BaseModel):

    @staticmethod
    def validate_password(value):
        if not RE_PASSWORD.match(value):
            raise InvalidDataError(ErrorsMsgEnum.ERROR_PASSWORD_WEAK)
        return value


class ValidationUserNameModel(BaseModel):

    @staticmethod
    def validate_username(value):
        if not RE_USERNAME.match(value):
            raise InvalidDataError(ErrorsMsgEnum.ERROR_USERNAME_INVALID)
        return value


class ValidationRoleModel(BaseModel):

    @staticmethod
    def validate_role(value):
        try:
            UserRolesEnum(value)
            return value
        except ValueError:
            raise InvalidDataError(ErrorsMsgEnum.ERROR_ROLE_INVALID)


class SearchModel(BaseModel):
    limit: Optional[int] = 20

    @field_validator("limit")
    def model_validate_limit(cls, value):
        if not 0 < value <= 100:
            raise InvalidDataError(ErrorsMsgEnum.ERROR_LIMIT)


class GenericIdModel(BaseModel):
    id: int = Field()


class StringSearchModel(SearchModel):
    search_query: str = Field(max_length=40)


class IdSearchModel(GenericIdModel, SearchModel):
    pass
