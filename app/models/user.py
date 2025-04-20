from pydantic import validator, EmailStr
from pydantic.fields import Field
from pydantic.main import BaseModel
from common import ValidationModel

class UserRead(BaseModel):
    username: str = Field(max_length=24)
    id: int = Field()

class UserSuRead(BaseModel):
    username: str = Field(max_length=24)
    password: str = Field(max_length=32)
    email: EmailStr

class UserUpdateName(ValidationModel):
    username: str = Field(max_length=24)

    @validator("username")
    def validate_username(cls , value):
        return cls.validate_username(value)

class UserUpdatePassword(ValidationModel):
    password: str = Field(max_length=32)

    @validator("password")
    def validate_password(cls , value):
        return cls.validate_password(value)

class UserUpdateRole(ValidationModel):
    role: str = Field(max_length=10)
    @validator("role")
    def validate_role(cls, value):
        return cls.validate_role(value)

class UserUpdateEmail(ValidationModel):
    email: EmailStr

class UserRegister(ValidationModel):
    username: str = Field(max_length=24)
    password: str = Field(max_length=32)
    email: EmailStr

    @validator("username")
    def validate_username(cls , value):
        return cls.validate_username(value)

    @validator("password")
    def validate_password(cls , value):
        return cls.validate_password(value)