from pydantic import field_validator, EmailStr
from pydantic.fields import Field
from pydantic.main import BaseModel
from typing import Optional
from datetime import datetime
from .common import ValidationTextModel, GenericIdModel


class ArticleCreateModel(ValidationTextModel):
    title: str = Field(max_length=32)
    text_content: str = Field(max_length=8000)
    course_id: int = Field()
    next_article: Optional[int] = None
    previous_article: Optional[int] = None

    @field_validator("title")
    def model_validate_title(cls, value):
        return cls.validate_text_content(value)

    @field_validator("text_content")
    def model_validate_text_content(cls, value):
        return cls.validate_text_content(value)


class ArticleGetModel(ArticleCreateModel, GenericIdModel):
    user_id: int = Field()
    date_posted: Optional[datetime] = None


class ArticleUpdateModel(ArticleCreateModel, GenericIdModel):
    pass
