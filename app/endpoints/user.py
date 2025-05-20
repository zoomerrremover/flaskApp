from http import HTTPStatus
from flask import Blueprint, render_template, Response, request, jsonify, g
from app.decorators import validate_model_params, require_auth
from app.models.user import UserUpdateModel
from app.db.service.user_service import update_user_by_id, delete_user_by_id, get_user_by_id
from app.common import serialize_response
from app.models.user import UserGetModel

user_route = Blueprint('user_route', __name__, url_prefix='/user')

@user_route.route("/", methods=['GET'])
@require_auth()
def get_user():
    user_id = g.current_user.id
    return serialize_response(UserGetModel, get_user_by_id(user_id))


@user_route.route("/", methods=['PATCH'])
@require_auth()
@validate_model_params(UserUpdateModel)
def update_user(data: UserUpdateModel):
    user_id = g.current_user.id
    update_user_by_id(user_id, **data.dict())
    return "", HTTPStatus.OK


@user_route.route("/", methods=['DELETE'])
@require_auth()
def delete_user():
    user_id = g.current_user.id
    delete_user_by_id(user_id)
    return "", HTTPStatus.OK
