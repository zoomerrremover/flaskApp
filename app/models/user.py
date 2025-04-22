from pydantic import validator, EmailStr
from pydantic.fields import Field
from pydantic.main import BaseModel
from app.models.common import ValidationTextModel, ValidationUserNameModel,ValidationPasswordModel, ValidationRoleModel


class UserRead(BaseModel):
    username: str = Field(max_length=24)


class UserSuRead(BaseModel):
    username: str = Field(max_length=24)
    email: EmailStr


class UserUpdateName(ValidationUserNameModel):
    username: str = Field(max_length=24)

    @validator("username")
    def model_validate_username(cls , value):
        return cls.validate_username(value)


class UserUpdatePassword(ValidationPasswordModel):
    password: str = Field(max_length=32)

    @validator("password")
    def model_validate_password(cls , value):
        return cls.validate_password(value)


class UserUpdateRole(ValidationRoleModel):
    role: str = Field(max_length=10)

    @validator("role")
    def model_validate_role(cls, value):
        return cls.validate_role(value)


class UserUpdateEmail(BaseModel):
    email: EmailStr


class UserRegister(ValidationUserNameModel,ValidationPasswordModel):
    username: str = Field(max_length=24)
    password: str = Field(max_length=32)
    email: EmailStr

    @validator("username")
    def model_validate_username(cls , value):
        return cls.validate_username(value)

    @validator("password")
    def model_validate_password(cls , value):
        return cls.validate_password(value)