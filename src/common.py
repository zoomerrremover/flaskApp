from flask import g
from pydantic.main import BaseModel
from email_validator import validate_email, EmailNotValidError
from src.constants import UserRolesEnum
from src.exceptions import NothingFoundError
from src.db import TextContentDbModel
from src.exceptions import AuthorizationError, InvalidDataError
from src.constants import ErrorsMsgEnum


def is_valid_email(email: str):
    try:
        validate_email(email, check_deliverability=True)
    except EmailNotValidError:
        raise InvalidDataError(ErrorsMsgEnum.ERROR_EMAIL_INVALID)


def user_role_is_satisfactory(
        role_input: str,
        role_required: UserRolesEnum
) -> bool:
    if role_input == UserRolesEnum.ADMIN:
        result = True
    elif role_input == UserRolesEnum.EDITOR:
        result = role_required in (UserRolesEnum.EDITOR, UserRolesEnum.USER)
    else:
        result = role_required == UserRolesEnum.USER
    return result


def owner_or_editor_check(media: TextContentDbModel):
    author = g.current_user
    if (
        not media or
        not author or
        not user_role_is_satisfactory(author.role, UserRolesEnum.EDITOR) and
        media.user_id != author.id
    ):
        raise AuthorizationError(ErrorsMsgEnum.ERROR_ROLE_INVALID)


def serialize_response(model: type[BaseModel], content):
    if isinstance(content, list):
        if len(content) == 0:
            raise NothingFoundError
        result = [
            model(
                **data.as_dict()
            ).model_dump(
                mode='json'
            ) for data in content
        ]
    elif content is None:
        raise NothingFoundError
    else:
        result = model(**content.as_dict()).model_dump(mode='json')
    return result
