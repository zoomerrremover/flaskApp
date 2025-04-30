from flask import Blueprint, render_template, abort, Response
from http import HTTPStatus
from app.decorators import validate_request, validate_request_params
from app.models.user import UserRegister
from app.db.service.service import create_user, get_username_is_original, get_email_is_valid
from app.settings import ERR_USERNAME_ORIGINAL, ERR_USERNAME_VALIDITY, RE_USERNAME
from app.security.security import generate_json_jwt
from pydantic.main import ValidationError

registration_route = Blueprint('registration_route', __name__, url_prefix='/registration')

@registration_route.route("/", methods=['POST'])
@validate_request(UserRegister)
def route_register_user(data: UserRegister):
    if get_username_is_original(data.username) and get_email_is_valid(data.email):
        user = create_user(data.username, data.password, data.email)
        return generate_json_jwt(user)
    else:
        raise ValidationError(ERR_USERNAME_ORIGINAL)


@registration_route.route("/", methods=['GET'])
@validate_request_params("username")
def route_name_check(username:str):
    if not RE_USERNAME.compile(username):
        raise ValidationError(ERR_USERNAME_VALIDITY)
    elif not get_username_is_original(username):
        raise ValidationError(ERR_USERNAME_ORIGINAL)
    else:
        result = Response(HTTPStatus.OK, "The username is original")
    return result
