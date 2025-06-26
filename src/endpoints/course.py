from http import HTTPStatus
from flask import Blueprint, render_template, Response, request, jsonify, g
from datetime import datetime, timezone
from src.decorators import (
    validate_model_request,
    validate_model_params,
    handle_db_exception,
    require_auth,
)
from src.models import (
    CourseCreateModel,
    CourseUpdateModel,
    GenericIdModel,
    CourseGetModel,
    StringSearchModel,
    IdSearchModel,
)
from src.db import Course
from src.constants import UserRolesEnum, ErrorsMsgEnum
from src.common import serialize_response, owner_or_editor_check


course_route = Blueprint("course_route", __name__, url_prefix="/course")


@course_route.route("/", methods=["GET"])
@validate_model_params(GenericIdModel)
def get_course(data: GenericIdModel):
    return serialize_response(CourseGetModel, Course.get_by_id(data.id))


@course_route.route("/by_user", methods=["GET"])
@validate_model_params(IdSearchModel)
def get_course_by_user(data: IdSearchModel):
    return serialize_response(CourseGetModel, Course.get_by_user(data.id, data.limit))


@course_route.route("/by_category", methods=["GET"])
@validate_model_params(StringSearchModel)
def get_course_by_category(data: StringSearchModel):
    return serialize_response(
        CourseGetModel, Course.get_by_category(data.search_query, data.limit)
    )


@course_route.route("/", methods=["POST"])
@require_auth()
@validate_model_request(CourseCreateModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_COURSE_UPDATE_FAILED)
def create_course(data: CourseCreateModel):
    addon_data = {
        "user_id": g.current_user.id,
        "date_created": datetime.now(timezone.utc),
        "date_posted": (
            None
            if g.current_user.role == UserRolesEnum.USER
            else datetime.now(timezone.utc)
        ),
    }
    return serialize_response(
        CourseGetModel, Course(**data.model_dump(), **addon_data).save()
    )


@course_route.route("/", methods=["PATCH"])
@require_auth()
@validate_model_params(CourseUpdateModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_COURSE_UPDATE_FAILED)
def update_course(data: CourseUpdateModel):
    owner_or_editor_check(Course.get_by_id(data.id))
    Course.update_by_id(data.id, **data.model_dump(exclude={"id"}))
    return "", HTTPStatus.OK


@course_route.route("/", methods=["DELETE"])
@require_auth()
@validate_model_params(GenericIdModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_DELETE_FAILED)
def delete_course(data: GenericIdModel):
    owner_or_editor_check(Course.get_by_id(data.id))
    Course.delete_by_id(data.id)
    return "", HTTPStatus.OK
