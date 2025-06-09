from pydantic import field_validator, EmailStr
from pydantic.fields import Field
from pydantic.main import BaseModel
from typing import Optional
from datetime import datetime
from src.models.common import GenericIdModel, ValidationTextModel


class CourseCreateModel(ValidationTextModel):
    title: str = Field(max_length=32)
    text_content: str = Field(max_length=8000)
    category: str = Field(max_length=24)

    @field_validator("title")
    def model_validate_title(cls, value):
        return cls.validate_text_content(value)

    @field_validator("text_content")
    def model_validate_text_content(cls, value):
        return cls.validate_text_content(value)


class CourseGetModel(CourseCreateModel, GenericIdModel):
    user_id: int = Field()
    date_posted: Optional[datetime] = None


class CourseUpdateModel(CourseCreateModel, GenericIdModel):
    pass
