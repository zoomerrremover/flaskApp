from flask import Blueprint, Response
from http import HTTPStatus
from app.decorators import validate_model_request, validate_model_params, handle_exception
from app.models.user import UserUsernameModel, UserUpdateModel
from app.db.service.user import UserDbService
from app.exceptions import ConflictingDataError
from app.constants import ErrorsMsgEnum
from app.security.jwt_service import generate_json_jwt
from sqlalchemy.exc import IntegrityError
from email_validator import EmailNotValidError

registration_route = Blueprint('registration_route', __name__, url_prefix='/registration')


@registration_route.route("/", methods=['POST'])
@validate_model_request(UserUpdateModel)
@handle_exception(IntegrityError, ConflictingDataError(ErrorsMsgEnum.ERR_USERNAME_ORIGINAL))
def register_user(data: UserUpdateModel):
    UserDbService.is_valid_email(data.email)
    user = UserDbService.create(**data.dict())
    return generate_json_jwt(user)
