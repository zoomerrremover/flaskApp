from pydantic import validator
from pydantic.fields import Field
from pydantic.main import BaseModel
from datetime import datetime

class PostRead(BaseModel):
    title: str = Field(max_length=32)
    text_content: str = Field(max_length=4000)
    date_posted: datetime = Field
    author: str = Field

class CreatePost(BaseModel):
    title: str = Field(max_length = 32)
    text_content: str = Field(max_length=4000)
