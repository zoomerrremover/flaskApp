from flask import Blueprint, Response
from http import HTTPStatus
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from ..decorators import (
    validate_model_request,
    validate_model_params,
    handle_db_exception,
)
from ..models import UserUsernameModel, UserUpdateModel
from ..db import User
from ..exceptions import ConflictingDataError
from ..constants import ErrorsMsgEnum, UserRolesEnum
from ..security import generate_json_jwt, passwd_to_hash
from ..common import is_valid_email

registration_route = Blueprint(
    "registration_route", __name__, url_prefix="/registration"
)


@registration_route.route("/", methods=["POST"])
@validate_model_request(UserUpdateModel)
@handle_db_exception(
    IntegrityError, ConflictingDataError(ErrorsMsgEnum.ERROR_USERNAME_ORIGINAL)
)
def register_user(data: UserUpdateModel):
    is_valid_email(data.email)
    db_entry = data.dict()
    db_entry['password'] = passwd_to_hash(data.password)
    user = User(**db_entry, **{'role': UserRolesEnum.user, 'date_registered': datetime.utcnow()}).save()
    return generate_json_jwt(user)


@registration_route.route("/username_check", methods=["POST"])
@validate_model_params(UserUsernameModel)
def check_username(data: UserUsernameModel):
    if not User.get_user_by_name(data.username):
        return "", 200
    else:
        raise ConflictingDataError(ErrorsMsgEnum.ERROR_USERNAME_ORIGINAL)
