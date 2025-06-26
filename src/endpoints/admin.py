from flask import Blueprint
from http import HTTPStatus
from src.db import User
from src.decorators import (
    validate_model_request,
    handle_db_exception,
    require_auth
)
from src.models import (
    UserRoleUpdateModel,
    GenericIdModel,
)
from src.constants import UserRolesEnum, ErrorsMsgEnum
from src.exceptions import AuthorizationError


admin_route = Blueprint("admin_route", __name__, url_prefix="/admin")


@admin_route.route("/user_role", methods=["PATCH"])
@require_auth(UserRolesEnum.ADMIN)
@validate_model_request(UserRoleUpdateModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_USER_UPDATE_FAILED)
def update_user_role(data: UserRoleUpdateModel):
    user_changed = User.get_by_id(data.id)
    if user_changed.role == UserRolesEnum.ADMIN:
        User.update_by_id(data.id, **data.dict())
        return "", HTTPStatus.NO_CONTENT
    else:
        raise AuthorizationError(ErrorsMsgEnum.ERROR_ROLE_INVALID)


@admin_route.route("/delete_user", methods=["PATCH"])
@require_auth(UserRolesEnum.ADMIN)
@validate_model_request(GenericIdModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_DELETE_FAILED)
def delete_user_by_id(data: GenericIdModel):
    user_changed = User.get_by_id(data.id)
    if user_changed.role == UserRolesEnum.ADMIN:
        User.delete_by_id(data.id)
        return "", HTTPStatus.NO_CONTENT
    else:
        raise AuthorizationError(ErrorsMsgEnum.ERROR_ROLE_INVALID)
