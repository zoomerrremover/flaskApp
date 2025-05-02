from flask import Blueprint, Response
from http import HTTPStatus
from app.decorators import validate_model_request, validate_model_params
from app.models.user import UserRegister, UserRead
from app.db.service.user_service import (create_user, get_username_is_original,
                                         get_email_is_valid)
from app.errors import ConflictingData
from app.constants import Errors
from app.security.security import generate_json_jwt

registration_route = Blueprint('registration_route', __name__, url_prefix='/registration')


@registration_route.route("/", methods=['POST'])
@validate_model_request(UserRegister)
def register_user(data: UserRegister):
    if get_username_is_original(data.username) and get_email_is_valid(data.email):
        user = create_user(data.username, data.password, data.email)
        return generate_json_jwt(user)
    else:
        raise ConflictingData(Errors.ERR_USERNAME_ORIGINAL)


@registration_route.route("/check_username", methods=['GET'])
@validate_model_params(UserRead)
def name_check(username: str):
    if not get_username_is_original(username):
        raise ConflictingData(Errors.ERR_USERNAME_ORIGINAL)
    else:
        return Response(HTTPStatus.OK, "The username is original")
