from pydantic import validator, EmailStr
from pydantic.fields import Field
from pydantic.main import BaseModel
from typing import Optional
from app.models.common import ValidationUserNameModel, ValidationPasswordModel, ValidationRoleModel, GenericIdModel

class UserUsernameModel(ValidationUserNameModel):
    username: str = Field(max_length=24)

    @validator("username")
    def model_validate_username(cls, value):
        return cls.validate_username(value)


class UserRoleModel(ValidationRoleModel):
    role: str = Field(max_length=10)

    @validator("role")
    def model_validate_role(cls, value):
        return cls.validate_role(value)


class UserPasswordModel(ValidationPasswordModel):
    password: str = Field(max_length=32)

    @validator("password")
    def model_validate_password(cls, value):
        return cls.validate_password(value)


class UserGet(UserUsernameModel, UserRoleModel): pass


class UserAdminGet(UserUsernameModel, UserRoleModel):
    email: EmailStr


class UserLogIn(UserUsernameModel, UserPasswordModel):pass


class UserRoleUpdate(GenericIdModel, UserRoleModel): pass


class UserUpdate(UserUsernameModel, UserPasswordModel):
    email: EmailStr


class UserSearch(ValidationUserNameModel, ValidationPasswordModel):
    id: Optional[int] = None
    username: Optional[str] = None
    role: Optional[str] = None

    @validator("role")
    def model_validate_role(cls, value):
        return cls.validate_role(value)

    @validator("username")
    def model_validate_username(cls, value):
        return cls.validate_username(value)
