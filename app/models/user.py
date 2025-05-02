from pydantic import validator, EmailStr
from pydantic.fields import Field
from pydantic.main import BaseModel
from typing import Optional
from app.models.common import (ValidationUserNameModel, ValidationPasswordModel,
                               ValidationRoleModel)


class UserRead(ValidationUserNameModel, ValidationRoleModel):
    username: str = Field(max_length=24)
    role: str = Field(max_length=10)


class UserSuRead(ValidationUserNameModel, ValidationRoleModel):
    username: str = Field(max_length=24)
    role: str = Field(max_length=10)
    email: EmailStr

    @validator("role")
    def model_validate_role(cls, value):
        return cls.validate_role(value)

    @validator("username")
    def model_validate_username(cls, value):
        return cls.validate_username(value)


class UserRegister(ValidationUserNameModel, ValidationPasswordModel):
    username: str = Field(max_length=24)
    password: str = Field(max_length=32)
    email: EmailStr

    @validator("username")
    def model_validate_username(cls, value):
        return cls.validate_username(value)

    @validator("password")
    def model_validate_password(cls, value):
        return cls.validate_password(value)


class UserLogIn(ValidationUserNameModel, ValidationPasswordModel):
    username: str = Field(max_length=24)
    password: str = Field(max_length=32)

    @validator("username")
    def model_validate_username(cls, value):
        return cls.validate_username(value)

    @validator("password")
    def model_validate_password(cls, value):
        return cls.validate_password(value)


class UserUpdate(ValidationUserNameModel,
                 ValidationPasswordModel,
                 ValidationRoleModel):
    username: Optional[str] = Field(max_length=24)
    password: Optional[str] = Field(max_length=32)
    email: EmailStr

    @validator("username")
    def model_validate_username(cls, value):
        return cls.validate_username(value)

    @validator("password")
    def model_validate_password(cls, value):
        return cls.validate_password(value)


class UserRoleUpdate(ValidationRoleModel):
    id: int = Field()
    role: str = Field(max_length=10)

    @validator("role")
    def model_validate_role(cls, value):
        return cls.validate_role(value)


class UserGet(ValidationUserNameModel, ValidationPasswordModel):
    id: Optional[int] = None
    username: Optional[str] = None
    role: Optional[str] = None
    email: EmailStr = None

    @validator("role")
    def model_validate_role(cls, value):
        return cls.validate_role(value)

    @validator("username")
    def model_validate_username(cls, value):
        return cls.validate_username(value)

class UserDelete(BaseModel):
    id: Optional[int] = Field()
