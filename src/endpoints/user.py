from http import HTTPStatus
from flask import Blueprint, render_template, Response, request, jsonify, g
from sqlalchemy.exc import IntegrityError
from src.decorators import validate_model_params, handle_db_exception, require_auth
from src.models import UserUpdateModel, UserGetModel
from src.db import User
from src.common import serialize_response
from src.constants import ErrorsMsgEnum
from src.exceptions import InvalidDataError

user_route = Blueprint("user_route", __name__, url_prefix="/user")


@user_route.route("/", methods=["GET"])
@require_auth()
def get_user():
    user_id = g.current_user.id
    return serialize_response(UserGetModel, User.get_by_id(user_id))


@user_route.route("/", methods=["PATCH"])
@require_auth()
@validate_model_params(UserUpdateModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_USER_UPDATE_FAILED)
def update_user(data: UserUpdateModel):
    user_id = g.current_user.id
    User.update_by_id(user_id, **data.dict(exclude={"id"}))
    return "", HTTPStatus.OK


@user_route.route("/", methods=["DELETE"])
@require_auth()
@handle_db_exception(ErrorsMsgEnum.ERROR_DELETE_FAILED)
def delete_user():
    user_id = g.current_user.id
    User.delete_by_id(user_id)
    return "", HTTPStatus.OK
