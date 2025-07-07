from datetime import datetime
from typing import Optional

from pydantic import field_validator
from pydantic.fields import Field

from src.models.common import GenericIdModel, StringSearchModel, ValidationTextModel


class SuggestionCreateModel(ValidationTextModel):
    title: str = Field(max_length=32)
    text_content: str = Field(max_length=8000)
    article_id: int = Field()

    @field_validator("title")
    def model_validate_title(cls, value):
        return cls.validate_text_content(value)

    @field_validator("text_content")
    def model_validate_text_content(cls, value):
        return cls.validate_text_content(value)


class SuggestionGetModel(SuggestionCreateModel, GenericIdModel):
    user_id: int = Field()
    date_posted: Optional[datetime] = None
    stars_count: int = Field()


class SuggestionUpdateModel(SuggestionCreateModel, GenericIdModel):
    pass


class SuggestionSearchModel(StringSearchModel):
    article_id: int = Field()
