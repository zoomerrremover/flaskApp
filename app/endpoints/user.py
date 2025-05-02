from flask import Blueprint, render_template, Response, request, jsonify
from app.constants import UserRole
from app.decorators import validate_model_request, validate_model_params, require_auth
from app.models.user import UserUpdate, UserGet, UserDelete
from app.db.service.user_service import (get_all_users, update_user_by_id,
                                         delete_user_by_id, get_user_by_id,
                                         get_users_by_name, get_su_users_by_email,
                                         get_users_by_role)

user_route = Blueprint('user_route', __name__, url_prefix='/users')


@user_route.route("/", methods=['GET'])
@validate_model_params(UserGet)
def get_users(model: UserGet):
    user_id = model.id
    username = model.username
    role = model.role
    if user_id:
        return jsonify(get_user_by_id(user_id))
    elif username:
        users = get_users_by_name(username)
    elif role:
        users = get_users_by_role(role)
    else:
        users = get_all_users()
    return jsonify([data.model_dump() for data in users])


@user_route.route("/", methods=['PATCH'])
@require_auth()
@validate_model_request(UserUpdate)
def update_user(data: UserUpdate):
    user_id = request.current_user.id
    return update_user_by_id(user_id,**data.dict())


@user_route.route("/role", methods=['PATCH'])
@require_auth(UserRole.admin)
@validate_model_request(UserUpdate)
def update_user_role(data: UserUpdate):
    user_id = request.current_user.id
    return update_user_by_id(user_id,**data.dict())


@user_route.route("/", methods=['DELETE'])
@require_auth(UserRole.admin)
@validate_model_params(UserDelete)
def delete_user(data: UserDelete):
    user_id = data.id
    return delete_user_by_id(user_id)
