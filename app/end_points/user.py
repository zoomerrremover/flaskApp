from flask import Blueprint, render_template, abort, Response, request
from http import HTTPStatus

user_route = Blueprint('user_route', __name__,
                        template_folder='templates')

@user_route.route("/",methods=['POST'])
def create_user():
    return Response("Not Implemented",HTTPStatus.NOT_IMPLEMENTED)

@user_route.route("/",methods=['GET'])
def get_user():
    return Response("Not Implemented",HTTPStatus.NOT_IMPLEMENTED)

@user_route.route("/name",methods=['GET'])
def get_by_name_user():
    return Response("Not Implemented",HTTPStatus.NOT_IMPLEMENTED)

@user_route.route("/",methods=['PUT'])
def update_user():
    return Response("Not Implemented",HTTPStatus.NOT_IMPLEMENTED)

@user_route.route("/",methods=['DELETE'])
def delete_user():
    return Response("Not Implemented",HTTPStatus.NOT_IMPLEMENTED)