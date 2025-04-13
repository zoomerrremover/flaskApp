from flask import Blueprint, render_template, abort, Response, request
from http import HTTPStatus

post_route = Blueprint('post_route', __name__,
                        template_folder='templates')

@post_route.route("/",methods=['POST'])
def create_post():
    return Response("Not Implemented",HTTPStatus.NOT_IMPLEMENTED)


@post_route.route("/",methods=['GET'])
def create_post():
    return Response("Not Implemented",HTTPStatus.NOT_IMPLEMENTED)

@post_route.route("/name",methods=['GET'])
def create_post():
    return Response("Not Implemented",HTTPStatus.NOT_IMPLEMENTED)

@post_route.route("/",methods=['PUT'])
def create_post():
    return Response("Not Implemented",HTTPStatus.NOT_IMPLEMENTED)


@post_route.route("/",methods=['DELETE'])
def create_post():
    return Response("Not Implemented",HTTPStatus.NOT_IMPLEMENTED)
