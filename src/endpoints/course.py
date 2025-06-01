from http import HTTPStatus
from flask import Blueprint, render_template, Response, request, jsonify, g
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from ..decorators import (
    validate_model_request,
    validate_model_params,
    handle_db_exception,
    require_auth,
)
from ..models import (
    CourseCreateModel,
    CourseUpdateModel,
    GenericIdModel,
    CourseGetModel,
)
from ..db import Course
from ..constants import UserRolesEnum, ErrorsMsgEnum
from ..exceptions import InvalidDataError
from ..common import serialize_response, owner_or_editor_check

course_route = Blueprint("course_route", __name__, url_prefix="/course")


@course_route.route("/", methods=["GET"])
@validate_model_params(GenericIdModel)
def get_course(data: GenericIdModel):
    return serialize_response(CourseGetModel, Course.get_by_id(data.id).save())


@course_route.route("/", methods=["POST"])
@require_auth()
@validate_model_request(CourseCreateModel)
@handle_db_exception(
    IntegrityError, InvalidDataError(ErrorsMsgEnum.ERROR_COURSE_UPDATE_CREATE)
)
def create_course(data: CourseCreateModel):
    addon_data = {
        "user_id": g.current_user.id,
        "date_created": datetime.utcnow(),
        "date_posted": (
            None if g.current_user.role == UserRolesEnum.user else datetime.utcnow()
        ),
    }
    return serialize_response(
        CourseGetModel, Course(**data.dict(), **addon_data).save()
    )


@course_route.route("/", methods=["PATCH"])
@require_auth()
@validate_model_params(CourseUpdateModel)
@handle_db_exception(
    IntegrityError, InvalidDataError(ErrorsMsgEnum.ERROR_COURSE_UPDATE_CREATE)
)
def update_course(data: CourseUpdateModel):
    owner_or_editor_check(Course.get_by_id(data.id))
    Course.update_by_id(data.id, **data.dict(exclude={"id"}))
    return "", HTTPStatus.OK


@course_route.route("/", methods=["DELETE"])
@require_auth()
@validate_model_params(GenericIdModel)
@handle_db_exception(IntegrityError, InvalidDataError(ErrorsMsgEnum.ERROR_DELETE))
def delete_course(data: GenericIdModel):
    owner_or_editor_check(Course.get_by_id(data.id))
    Course.delete_by_id(data.id)
    return "", HTTPStatus.OK
