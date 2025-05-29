from http import HTTPStatus
from flask import Blueprint, render_template, Response, request, jsonify, g
from app.decorators import validate_model_params, handle_exception
from app.security.auth import require_auth
from app.models.user import UserUpdateModel
from app.db import User
from app.common import serialize_response
from app.models.user import UserGetModel
from sqlalchemy.exc import IntegrityError
from app.constants import ErrorsMsgEnum
from app.exceptions import InvalidDataError

user_route = Blueprint("user_route", __name__, url_prefix="/user")


@user_route.route("/", methods=["GET"])
@require_auth()
def get_user():
    user_id = g.current_user.id
    return serialize_response(UserGetModel, User.get_by_id(user_id))


@user_route.route("/", methods=["PATCH"])
@require_auth()
@validate_model_params(UserUpdateModel)
@handle_exception(IntegrityError, InvalidDataError(ErrorsMsgEnum.ERR_USER_UPDATE))
def update_user(data: UserUpdateModel):
    user_id = g.current_user.id
    User.update(user_id, **data.dict())
    return "", HTTPStatus.OK


@user_route.route("/", methods=["DELETE"])
@require_auth()
@handle_exception(IntegrityError, InvalidDataError(ErrorsMsgEnum.ERR_DELETE))
def delete_user():
    user_id = g.current_user.id
    User.delete(user_id)
    return "", HTTPStatus.OK
