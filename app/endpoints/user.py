from flask import Blueprint, render_template, Response, request, jsonify
from http import HTTPStatus
from app.decorators import validate_request, validate_request_params, require_auth
from app.models.user import UserUpdatePassword,UserUpdateName, UserUpdateRole, UserUpdateEmail
from app.db.service import create_user, get_users, update_user_by_id, delete_user_by_id, get_user_by_id, \
    get_users_by_name

user_route = Blueprint('user_route', __name__, url_prefix='/users')
@user_route.route("/",methods=['GET'])
def route_get_users():
    user_id = request.args.get('id')
    if user_id:
        return jsonify(get_user_by_id())
    username = request.args.get('username')
    users = get_users()
    if username:
        users = get_users_by_name(username)
    return jsonify([user.model_dump() for user in users])

@user_route.route("/password",methods=['PATCH'])
@require_auth()
@validate_request(UserUpdatePassword)
def route_update_user_password(data: UserUpdatePassword):
    user_id = request.current_user.id
    update_user_by_id(user_id,**data.dict())
    return Response("Password changed",HTTPStatus.OK)

@user_route.route("/username",methods=['PATCH'])
@require_auth()
@validate_request(UserUpdateName)
def route_update_user_name(data: UserUpdateName):
    user_id = request.current_user.id
    update_user_by_id(user_id,**data.dict())
    return Response("Name changed",HTTPStatus.OK)

@user_route.route("/role",methods=['PATCH'])
@validate_request_params("id")
@validate_request(UserUpdateRole)
def route_update_user_role(data: UserUpdateRole):
    user_id = request.args.get('id')
    update_user_by_id(user_id,**data.dict())
    return Response("Name changed",HTTPStatus.OK)

@user_route.route("/email",methods=['PATCH'])
@require_auth()
@validate_request(UserUpdateEmail)
def route_update_user_email(data: UserUpdateEmail):
    user_id = request.current_user.id
    update_user_by_id(user_id,**data.dict())
    return Response("Name changed",HTTPStatus.OK)

@user_route.route("/",methods=['DELETE'])
@validate_request_params("id")
def route_delete_user():
    user_id = request.args.get('id')
    delete_user_by_id(user_id)
    return Response("User deleted", HTTPStatus.OK)
