from flask import Blueprint, render_template, Response, request, jsonify
from app.db import User
from app.decorators import validate_model_request, handle_exception
from app.security.auth import require_auth
from app.models.user import UserRoleUpdateModel, UserEmailModel, UserRoleModel
from app.constants import UserRolesEnum
from app.models.common import GenericIdModel
from sqlalchemy.exc import IntegrityError
from app.exceptions import InvalidDataError
from app.constants import ErrorsMsgEnum
from http import HTTPStatus

admin_route = Blueprint("admin_route", __name__, url_prefix="/admin")


@admin_route.route("/user_role", methods=["PATCH"])
@require_auth(UserRolesEnum.admin)
@validate_model_request(UserRoleUpdateModel)
@handle_exception(IntegrityError, InvalidDataError(ErrorsMsgEnum.ERR_USER_UPDATE))
def update_user_role(data: UserRoleUpdateModel):
    # TODO: Add additional safety checks ( Check if user in question is not admin, etc)
    User.update(data.id, **data.dict())
    return "", HTTPStatus.NO_CONTENT


@admin_route.route("/delete_user", methods=["PATCH"])
@require_auth(UserRolesEnum.admin)
@validate_model_request(GenericIdModel)
@handle_exception(IntegrityError, InvalidDataError(ErrorsMsgEnum.ERR_DELETE))
def delete_user_by_id(data: GenericIdModel):
    # TODO: Add additional safety checks  ( Check if user in question is not admin, etc)
    User.delete(data.id)
    return "", HTTPStatus.NO_CONTENTs
