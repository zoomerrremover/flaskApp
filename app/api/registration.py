from flask import Blueprint, render_template, abort
from http import HTTPStatus

registration_route = Blueprint('user_route', __name__,
                        template_folder='templates')

@registration_route.route("/",methods=['POST'])
def create_user():
    return Response("Not Implemented",HTTPStatus.NOT_IMPLEMENTED)
