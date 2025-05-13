from pydantic import validator, EmailStr
from pydantic.fields import Field
from pydantic.main import BaseModel
from typing import Optional
from datetime import datetime
from app.models.common import  ValidationTextModel

class ArticleCreate(ValidationTextModel):
    title: str = Field(max_length=32)
    text_content: str = Field(max_length=8000)

    @validator("title")
    def model_validate_title(cls, value):
        return cls.validate_text_content(value)

    @validator("text_content")
    def model_validate_text_content(cls, value):
        return cls.validate_text_content(value)


class ArticleGet(ArticleCreate):
    author: int = Field(max_length=24)
    date_posted: datetime = Field()


class ArticleUpdate(ArticleCreate):
    id: int = Field()


class ArticleSearch(BaseModel):
    id:  Optional[int] = None
    title: Optional[str] = None
    author: Optional[int] = None
    text_content: Optional[str] = None
    date_posted: Optional[datetime] = None
