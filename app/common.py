from fuzzywuzzy import fuzz
from app.constants import UserRole
from flask import jsonify, Response, g
from pydantic.main import BaseModel
from app.exceptions import NothingFoundError
from app.db.models import TextContentDbModel
from app.exceptions import AuthorizationError
from app.constants import Errors

def str_compare(base_string: str, string_to_compare: str, index: int) -> bool:
    return fuzz.ratio(base_string, string_to_compare) > index


def user_role_is_satisfactory(role_input: UserRole, role_required: UserRole) -> bool:
    if role_input == UserRole.admin:
        result = True
    elif role_input == UserRole.editor:
        result = role_required == UserRole.editor or role_required == UserRole.user
    else:
        result = role_required == UserRole.user
    return result


def owner_or_editor_check(media: TextContentDbModel):
    author = g.current_user
    if user_role_is_satisfactory(author.role, UserRole.editor) or media.user_id != author.id:
        raise AuthorizationError(Errors.ERR_UNSATISFACTORY_ROLE)


def serialize_response(model: type[BaseModel], content):
    if isinstance(content, list):
        result = [model(**data.as_dict()) for data in content]
    elif content is None:
        raise NothingFoundError
    else:
        result = model(**content.as_dict())
    return result.json()
