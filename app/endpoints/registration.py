from flask import Blueprint, render_template, abort, Response
from http import HTTPStatus
from app.decorators import validate_request, validate_request_params
from app.models.user import UserRegister
from app.db.service import create_user, get_username_is_original, get_email_is_valid
from app.settings import ERR_USERNAME_ORIGINAL, ERR_USERNAME_VALIDITY, RE_USERNAME
from app.security.security import generate_json_jwt

registration_route = Blueprint('registration_route', __name__, url_prefix='/registration')

@registration_route.route("/",methods=['POST'])
@validate_request(UserRegister)
def route_register_user(data: UserRegister):
    result = Response(HTTPStatus.CONFLICT,ERR_USERNAME_ORIGINAL)
    if get_username_is_original(data.username) and get_email_is_valid(data.email):
        user = create_user(data.username, data.password, data.email)
        result = generate_json_jwt(user)
    return result

@validate_request_params("username")
@registration_route.route("/",methods=['GET'])
def route_name_check(username:str):
    result = Response(HTTPStatus.OK,"The username is original")
    if not RE_USERNAME.compile(username):
        result = Response(HTTPStatus.CONFLICT,ERR_USERNAME_VALIDITY)
    elif not get_user_name_is_original(username):
        result = Response(HTTPStatus.CONFLICT, ERR_USERNAME_ORIGINAL)
    return result