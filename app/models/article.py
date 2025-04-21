from pydantic import validator
from pydantic.fields import Field
from pydantic.main import BaseModel
from datetime import datetime
from app.models.common import ValidationModel

class ShowArticle(BaseModel):
    title:str = Field(maxlength = "32")
    text_content: str = Field(maxlength = "8000")
    date_posted: datetime = Field()
    #Do we send reference data ?

class CreateArticle(ValidationModel):
    title:str = Field(maxlength = "32")
    text_content: str = Field(maxlength="8000")
    # Do we send reference data ?
    @validator("title")
    def validate_title(cls, value):
        return cls.validate_text_content(value)

    @validator("text_content")
    def validate_text_content(cls, value):
        return cls.validate_text_content(value)

class UpdateArticle(ValidationModel):
    title:str = Field(maxlength = "32")
    text_content: str = Field(maxlength="8000")
    # Do we send reference data ?
    @validator("title")
    def validate_title(cls, value):
        return cls.validate_text_content(value)

    @validator("text_content")
    def validate_text_content(cls, value):
        return cls.validate_text_content(value)