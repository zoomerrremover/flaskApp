from pydantic import validator, EmailStr
from pydantic.fields import Field
from pydantic.main import BaseModel
from typing import Optional
from datetime import datetime
from app.models.common import  ValidationTextModel

class ArticleGet(BaseModel):
    title: str = Field(max_length=32)
    author: int = Field(max_length=24)
    text_content: str = Field(max_length=8000)
    date_posted: datetime = Field()


class ArticleCreate(ValidationTextModel):
    title: str = Field(max_length=32)
    text_content: str = Field(max_length=8000)

    @validator("title")
    def model_validate_title(cls, value):
        return cls.validate_text_content(value)

    @validator("text_content")
    def model_validate_text_content(cls, value):
        return cls.validate_text_content(value)


class ArticleUpdate(ValidationTextModel):
    id: int = Field()
    title: str = Field(max_length=32)
    text_content: str = Field(max_length=8000)

    @validator("title")
    def model_validate_title(cls, value):
        return cls.validate_text_content(value)

    @validator("text_content")
    def model_validate_text_content(cls, value):
        return cls.validate_text_content(value)


class ArticleSearch(BaseModel):
    title: Optional[str] = Field(max_length=32)
    author: Optional[int] = Field(max_length=24)
    text_content: Optional[str] = Field(max_length=8000)
    date_posted: Optional[datetime] = Field()
