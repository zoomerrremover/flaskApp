from datetime import datetime
from typing import Optional

from pydantic import field_validator
from pydantic.fields import Field

from src.models.common import GenericIdModel, StringSearchModel, ValidationTextModel


class ArticleCreateModel(ValidationTextModel):
    title: str = Field(max_length=100)
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


class ArticleSearchModel(StringSearchModel):
    course_id: int = Field()
