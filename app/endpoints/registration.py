from flask import Blueprint, Response
from http import HTTPStatus
from app.decorators import validate_model_request, validate_model_params, handle_exception
from app.models.user import UserUsernameModel, UserUpdateModel
from app.db.service.user import create_user, get_username_is_original, get_email_is_valid
from app.exceptions import ConflictingDataError
from app.constants import ErrorsMsgEnum
from app.security.jwt_service import generate_json_jwt
from sqlalchemy.exc import IntegnityError
from email_validator import EmailNotValidError

registration_route = Blueprint('registration_route', __name__, url_prefix='/registration')


@registration_route.route("/", methods=['POST'])
@validate_model_request(UserUpdateModel)
@handle_exception(IntegnityError, ConflictingDataError(ErrorsMsgEnum.ERR_USERNAME_ORIGINAL))
@handle_exception(EmailNotValidError, ConflictingDataError(ErrorsMsgEnum.ERR_EMAIL_VALID))
def register_user(data: UserUpdateModel):
    get_email_is_valid(data.email)
    user = create_user(data.username, data.password, data.email)
    return generate_json_jwt(user)


@registration_route.route("/check_username", methods=['GET'])
@validate_model_params(UserUsernameModel)
def name_check(data: UserUsernameModel):
    if not get_username_is_original(data.username):
        raise ConflictingDataError(ErrorsMsgEnum.ERR_USERNAME_ORIGINAL)
    else:
        return "", HTTPStatus.OK
