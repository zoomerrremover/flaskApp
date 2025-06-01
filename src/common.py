from flask import jsonify, Response, g
from pydantic.main import BaseModel
from email_validator import validate_email, EmailNotValidError
from .constants import UserRolesEnum
from .exceptions import NothingFoundError
from .db import TextContentDbModel
from .exceptions import AuthorizationError
from .constants import ErrorsMsgEnum


def is_valid_email(email: str):
    try:
        validate_email(email, check_deliverability=True)
    except EmailNotValidError:
        raise InvalidDataError(ErrorsMsgEnum.ERROR_EMAIL_VALID)


def user_role_is_satisfactory(role_input: str, role_required: UserRolesEnum) -> bool:
    if role_input == UserRolesEnum.admin:
        result = True
    elif role_input == UserRolesEnum.editor:
        result = role_required in (UserRolesEnum.editor, UserRolesEnum.user)
    else:
        result = role_required == UserRolesEnum.user
    return result


def owner_or_editor_check(media: TextContentDbModel):
    author = g.current_user
    if (
        user_role_is_satisfactory(author.role, UserRolesEnum.editor)
        or media.user_id != author.id
    ):
        raise AuthorizationError(ErrorsMsgEnum.ERRO_rUNSATISFACTORY_ROLE)


def serialize_response(model: type[BaseModel], content):
    if isinstance(content, list):
        result = [model(**data.as_dict()).json() for data in content]
    elif content is None:
        raise NothingFoundError
    else:
        result = model(**content.as_dict()).json()
    return result
