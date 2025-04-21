from pydantic import validator
from pydantic.fields import Field
from pydantic.main import BaseModel
from datetime import datetime
from app.models.common import ValidationTextModel

class ShowSuggestion(BaseModel):
    title:str = Field(maxlength = "32")
    text_content: str = Field(maxlength = "8000")
    date_posted: datetime = Field()
    up_vote: int = Field()
    down_vote: int = Field()
    #Do we send reference data ?

class CreateSuggestion(ValidationTextModel):
    title:str = Field(maxlength = "32")
    text_content: str = Field(maxlength="8000")
    # Do we send reference data ?
    @validator("title")
    def validate_title(cls, value):
        return cls.validate_text_content(value)

    @validator("text_content")
    def validate_text_content(cls, value):
        return cls.validate_text_content(value)

class UpdateSuggestion(ValidationTextModel):
    title:str = Field(maxlength = "32")
    text_content: str = Field(maxlength="8000")
    # Do we send reference data ?
    @validator("title")
    def validate_title(cls, value):
        return cls.validate_text_content(value)

    @validator("text_content")
    def validate_text_content(cls, value):
        return cls.validate_text_content(value)