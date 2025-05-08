from pydantic import validator, EmailStr
from pydantic.fields import Field
from pydantic.main import BaseModel
from typing import Optional
from app.models.common import ValidationUserNameModel, ValidationPasswordModel, ValidationRoleModel