from http import HTTPStatus
from flask import Blueprint, render_template, Response, request, jsonify, g
from app.decorators import (
    validate_model_request,
    validate_model_params,
    handle_exception,
)
from app.security.auth import require_auth
from app.models.course import CourseCreateModel, CourseUpdateModel
from app.db import Course
from app.models.common import GenericIdModel
from app.constants import UserRolesEnum, ErrorsMsgEnum
from app.exceptions import InvalidDataError
from datetime import datetime
from app.common import serialize_response, owner_or_editor_check
from app.models.course import CourseGetModel
from sqlalchemy.exc import IntegrityError

course_route = Blueprint("course_route", __name__, url_prefix="/course")


@course_route.route("/", methods=["GET"])
@validate_model_params(GenericIdModel)
def get_course(data: GenericIdModel):
    return serialize_response(CourseGetModel, Course.get_by_id(data.id).save())


@course_route.route("/", methods=["POST"])
@require_auth()
@validate_model_request(CourseCreateModel)
@handle_exception(
    IntegrityError, InvalidDataError(ErrorsMsgEnum.ERR_COURSE_UPDATE_CREATE)
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
        CourseGetModel, Course.create(**data.dict(), **addon_data)
    )


@course_route.route("/", methods=["PATCH"])
@require_auth()
@validate_model_params(CourseUpdateModel)
@handle_exception(
    IntegrityError, InvalidDataError(ErrorsMsgEnum.ERR_COURSE_UPDATE_CREATE)
)
def update_course(data: CourseUpdateModel):
    owner_or_editor_check(Course.get_by_id(data.id))
    Course.update(data.id, **data.dict(exclude={"id"}))
    return "", HTTPStatus.OK


@course_route.route("/", methods=["DELETE"])
@require_auth()
@validate_model_params(GenericIdModel)
@handle_exception(IntegrityError, InvalidDataError(ErrorsMsgEnum.ERR_DELETE))
def delete_course(data: GenericIdModel):
    owner_or_editor_check(Course.get_by_id(data.id))
    Course.delete(data.id)
    return "", HTTPStatus.OK
