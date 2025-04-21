from flask import Blueprint, render_template, abort
from http import HTTPStatus

auth_route = Blueprint('registration_route', __name__, url_prefix='/authentication')

@registration_route.route("/",methods=['POST'])
def register_user():
    return Response("Not Implemented",HTTPStatus.NOT_IMPLEMENTED)
