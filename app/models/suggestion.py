from pydantic import validator, EmailStr
from pydantic.fields import Field
from pydantic.main import BaseModel
from typing import Optional
from datetime import datetime
from app.models.common import GenericIdModel, ValidationTextModel


class SuggestionCreateModel(ValidationTextModel):
    title: str = Field(max_length=32)
    text_content: str = Field(max_length=8000)
    article_id: int = Field()

    @validator("title")
    def model_validate_title(cls, value):
        return cls.validate_text_content(value)

    @validator("text_content")
    def model_validate_text_content(cls, value):
        return cls.validate_text_content(value)


class SuggestionGetModel(SuggestionCreateModel, GenericIdModel):
    user_id: int = Field()
    date_posted: Optional[datetime] = None
    likes: int
    dislikes: int


class SuggestionUpdateModel(SuggestionCreateModel, GenericIdModel):
    pass


class SuggestionReactionModel(GenericIdModel):
    like: bool = Field()
