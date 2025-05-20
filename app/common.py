from fuzzywuzzy import fuzz
from app.constants import UserRolesEnum
from flask import jsonify, Response, g
from pydantic.main import BaseModel
from app.exceptions import NothingFoundError
from app.db.models.models import TextContentDbModel
from app.exceptions import AuthorizationError
from app.constants import ErrorsMsgEnum

def str_compare(base_string: str, string_to_compare: str, index: int) -> bool:
    return fuzz.ratio(base_string, string_to_compare) > index


def user_role_is_satisfactory(role_input: UserRolesEnum, role_required: UserRolesEnum) -> bool:
    if role_input == UserRolesEnum.admin:
        result = True
    elif role_input == UserRolesEnum.editor:
        result = role_required in (UserRolesEnum.editor, UserRolesEnum.user)
    else:
        result = role_required == UserRolesEnum.user
    return result


def owner_or_editor_check(media: TextContentDbModel):
    author = g.current_user
    if user_role_is_satisfactory(author.role, UserRolesEnum.editor) or media.user_id != author.id:
        raise AuthorizationError(ErrorsMsgEnum.ERR_UNSATISFACTORY_ROLE)


def serialize_response(model: type[BaseModel], content):
    if isinstance(content, list):
        result = [model(**data.as_dict()) for data in content]
    elif content is None:
        raise NothingFoundError
    else:
        result = model(**content.as_dict())
    return result.json()
