from flask import Blueprint, Response
from http import HTTPStatus
from app.decorators import validate_model_request, validate_model_params
from app.models.user import UserUsernameModel, UserUpdate
from app.db.service.user_service import (create_user, get_username_is_original,
                                         get_email_is_valid)
from app.exceptions import ConflictingDataError
from app.constants import Errors
from app.security.security import generate_json_jwt

registration_route = Blueprint('registration_route', __name__, url_prefix='/registration')


@registration_route.route("/", methods=['POST'])
@validate_model_request(UserUpdate)
def register_user(data: UserUpdate):
    get_username_is_original(data.username)
    get_email_is_valid(data.email)
    user = create_user(data.username, data.password, data.email)
    return generate_json_jwt(user)


@registration_route.route("/check_username", methods=['GET'])
@validate_model_params(UserUsernameModel)
def name_check(data: UserUsernameModel):
    if not get_username_is_original(data.username):
        raise ConflictingDataError(Errors.ERR_USERNAME_ORIGINAL)
    else:
        return HTTPStatus.NO_CONTENT
