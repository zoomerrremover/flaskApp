from flask import Blueprint, render_template, abort, Response, request
from http import HTTPStatus
from app.decorators import validate_request, serialize_response, validate_request_params
from app.models.user import *
from app.db.service import create_user,get_users, update_user_by_id, delete_user_by_id, get_user_by_id

user_route = Blueprint('user_route', __name__, url_prefix='/user')

@user_route.route("/",methods=['POST'])
@validate_request(UserCreate)
def route_create_user(data: UserCreate):
    create_user(**data.dict())
    return Response("User Create", HTTPStatus.OK)

@user_route.route("/",methods=['GET'])
@serialize_response(UserRead)
def route_get_user():
    users =  get_users()
    return [UserRead(
        username = data.username
    ) for data in users]

@user_route.route("/password",methods=['PATCH'])
@validate_request_params("id")
@validate_request(UserUpdatePassword)
def route_update_user_password(data: UserUpdatePassword):
    user_id = request.args.get('id')
    update_user_by_id(user_id,**data.dict())
    return Response("Password changed",HTTPStatus.OK)

@user_route.route("/",methods=['PATCH'])
@validate_request_params("id")
@validate_request(UserUpdateName)
def route_update_user(data: UserUpdateName):
    user_id = request.args.get('id')
    update_user_by_id(user_id,**data.dict())
    return Response("Name changed",HTTPStatus.OK)

@user_route.route("/",methods=['DELETE'])
@validate_request_params("id")
def route_delete_user():
    user_id = request.args.get('id')
    delete_user_by_id(user_id)
    return Response("User deleted", HTTPStatus.OK)