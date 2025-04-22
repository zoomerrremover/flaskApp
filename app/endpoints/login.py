from flask import Blueprint, render_template, abort, Response, jsonify
from http import HTTPStatus
from app.decorators import validate_request_params
from app.db.service import get_user_login
from app.security.security import generate_json_jwt

login_route = Blueprint('login_route', __name__, url_prefix='/login')

@login_route.route("/",methods=['POST'])
@validate_request_params('username','password')
def route_login(username:str,password:str):
    user = get_user_login(username,password)
    result = Response("Invalid credentials", status=HTTPStatus.FORBIDDEN)
    if user:
        result = generate_json_jwt(user)
    return result
