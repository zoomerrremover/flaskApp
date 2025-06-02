from flask import Blueprint, render_template, Response, request, jsonify
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from ..db import User
from ..decorators import validate_model_request, handle_db_exception, require_auth
from ..models import UserRoleUpdateModel, UserEmailModel, UserRoleModel, GenericIdModel
from ..constants import UserRolesEnum
from ..exceptions import InvalidDataError
from ..constants import ErrorsMsgEnum

admin_route = Blueprint("admin_route", __name__, url_prefix="/admin")


@admin_route.route("/user_role", methods=["PATCH"])
@require_auth(UserRolesEnum.admin)
@validate_model_request(UserRoleUpdateModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_USER_UPDATE_FAILED)
def update_user_role(data: UserRoleUpdateModel):
    # TODO: Add additional safety checks ( Check if user in question is not admin, etc)
    User.update_by_id(data.id, **data.dict())
    return "", HTTPStatus.NO_CONTENT


@admin_route.route("/delete_user", methods=["PATCH"])
@require_auth(UserRolesEnum.admin)
@validate_model_request(GenericIdModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_DELETE_FAILED)
def delete_user_by_id(data: GenericIdModel):
    # TODO: Add additional safety checks  ( Check if user in question is not admin, etc)
    User.delete_by_id(data.id)
    return "", HTTPStatus.NO_CONTENT
