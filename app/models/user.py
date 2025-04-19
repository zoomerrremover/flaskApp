from pydantic import validator
from pydantic.fields import Field
from pydantic.main import BaseModel

class UserRead(BaseModel):
    username: str = Field(max_length=24)

class UserUpdateName(BaseModel):
    username: str = Field(max_length=24)

class UserUpdatePassword(BaseModel):
    password: str = Field(max_length=32)

class UserCreate(BaseModel):
    username: str = Field(max_length=24)
    password: str = Field(max_length=32)