from flask import Blueprint, render_template, Response, request, jsonify
from app.constants import UserRole
from app.decorators import validate_model_request, validate_model_params, require_auth
from app.models.user import UserUpdate, UserSearch, UserDelete
from app.db.service.user_service import update_user_by_id, delete_user_by_id, get_user_by_id,

user_route = Blueprint('user_route', __name__, url_prefix='/user')

@user_route.route("/", methods=['GET'])
@require_auth()
@validate_model_params(UserSearch)
def get_user():
    user_id = request.current_user.id
    return get_user_by_id(user_id, True)


@user_route.route("/", methods=['PATCH'])
@require_auth()
@validate_model_request(UserUpdate)
def update_user(data: UserUpdate):
    user_id = request.current_user.id
    return update_user_by_id(user_id, **data.dict())


@user_route.route("/", methods=['DELETE'])
@require_auth(UserRole.admin)
@validate_model_params(UserSearch)
def delete_user(data: UserSearch):
    user_id = data.id
    return delete_user_by_id(user_id)
