from datetime import datetime

from pydantic import EmailStr, field_validator
from pydantic.fields import Field
from pydantic.main import BaseModel

from src.models.common import (
    GenericIdModel,
    ValidationPasswordModel,
    ValidationRoleModel,
    ValidationUserNameModel,
)


class UserUsernameModel(ValidationUserNameModel):
    username: str = Field(max_length=24)

    @field_validator("username")
    def model_validate_username(cls, value):
        return cls.validate_username(value)


class UserRoleModel(ValidationRoleModel):
    role: str = Field(max_length=10)

    @field_validator("role")
    def model_validate_role(cls, value):
        return cls.validate_role(value)


class UserPasswordModel(ValidationPasswordModel):
    password: str = Field(max_length=32)

    @field_validator("password")
    def model_validate_password(cls, value):
        return cls.validate_password(value)


class UserEmailModel(BaseModel):
    email: EmailStr


class UserGetModel(GenericIdModel):
    username: str = Field(max_length=24)
    role: str = Field(max_length=10)
    date_registered: datetime = Field()


class UserAdminGetModel(UserGetModel, UserEmailModel):
    pass


class UserLogInModel(UserUsernameModel, UserPasswordModel):
    pass


class UserRoleUpdateModel(GenericIdModel, UserRoleModel):
    pass


class UserUpdateModel(UserUsernameModel, UserPasswordModel, UserEmailModel):
    pass
