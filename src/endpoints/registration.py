from flask import Blueprint, Response
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from ..decorators import (
    validate_model_request,
    validate_model_params,
    handle_exception,
)
from ..models import UserUsernameModel, UserUpdateModel
from ..db import User
from ..exceptions import ConflictingDataError
from ..constants import ErrorsMsgEnum
from ..security import generate_json_jwt
from ..common import is_valid_email

registration_route = Blueprint(
    "registration_route", __name__, url_prefix="/registration"
)


@registration_route.route("/", methods=["POST"])
@validate_model_request(UserUpdateModel)
@handle_exception(
    IntegrityError, ConflictingDataError(ErrorsMsgEnum.ERR_USERNAME_ORIGINAL)
)
def register_user(data: UserUpdateModel):
    is_valid_email(data.email)
    user = User.create(**data.dict()).save()
    return generate_json_jwt(user)


@registration_route.route("/username_check", methods=["POST"])
@validate_model_params(UserUsernameModel)
def check_username(data: UserUsernameModel):
    if User.get_user_by_name(data.username):
        return "", 200
    else:
        raise ConflictingDataError(ErrorsMsgEnum.ERR_USERNAME_ORIGINAL)
