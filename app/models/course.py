from pydantic import validator
from pydantic.fields import Field
from pydantic.main import BaseModel
from datetime import datetime
from app.models.common import ValidationModel

class Course(BaseModel):
    title: str = Field(max_length=32)
    text_content: str = Field(max_length=4000)
    category: str = Field(max_length=20)
    date_posted: datetime = Field

class CreateCourse(ValidationModel):
    title: str = Field(max_length = 32)
    text_content: str = Field(max_length=4000)
    category: str = Field(max_length=20)
    date_posted: datetime = Field

    @validator("title")
    def validate_title(cls, value):
        return cls.validate_text_content(value)

    @validator("text_content")
    def validate_text_content(cls, value):
        return cls.validate_text_content(value)

    @validator("category")
    def validate_category(cls, value):
        return cls.validate_text_content(value)

class UpdateCourse(ValidationModel):
    title: str = Field(max_length = 32)
    text_content: str = Field(max_length=4000)
    category: str = Field(max_length=20)

    @validator("title")
    def validate_title(cls, value):
        return cls.validate_text_content(value)

    @validator("text_content")
    def validate_text_content(cls, value):
        return cls.validate_text_content(value)

    @validator("category")
    def validate_category(cls, value):
        return cls.validate_text_content(value)

