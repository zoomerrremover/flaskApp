from datetime import datetime, timezone
from http import HTTPStatus

from flask import Blueprint

from src.common import is_valid_email
from src.constants import ErrorsMsgEnum, UserRolesEnum
from src.db import User
from src.decorators import (
    handle_db_exception,
    validate_model_params,
    validate_model_request,
)
from src.exceptions import ConflictingDataError
from src.models import UserUpdateModel, UserUsernameModel
from src.security import generate_json_jwt, passwd_to_hash

registration_route = Blueprint(
    "registration_route", __name__, url_prefix="/registration"
)


@registration_route.route("/", methods=["POST"])
@validate_model_request(UserUpdateModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_USERNAME_NOT_ORIGINAL)
def register_user(data: UserUpdateModel):
    is_valid_email(data.email)
    db_entry = data.model_dump()
    db_entry["password"] = passwd_to_hash(data.password)
    user = User.create(
        **db_entry,
        **{
            "role": UserRolesEnum.USER,
            "date_registered": datetime.now(timezone.utc),
        }
    )
    return generate_json_jwt(user)


@registration_route.route("/username_check", methods=["POST"])
@validate_model_params(UserUsernameModel)
def check_username(data: UserUsernameModel):
    if not User.get_user_by_name(data.username):
        return "", HTTPStatus.OK
    else:
        raise ConflictingDataError(ErrorsMsgEnum.ERROR_USERNAME_NOT_ORIGINAL)
