from http import HTTPStatus
from flask import Blueprint, render_template, Response, request, jsonify, g
from app.decorators import validate_model_request, validate_model_params, require_auth
from app.models.course import CourseCreateModel, CourseUpdateModel
from app.db.service.course_service import get_course_by_id, create_course, update_course_by_id, delete_course_by_id
from app.models.common import GenericIdModel
from app.constants import UserRole
from datetime import datetime
from app.common import serialize_response, owner_or_editor_check
from app.models.course import CourseGetModel

course_route = Blueprint('course_route', __name__, url_prefix='/course')


@course_route.route("/", methods=['GET'])
@validate_model_params(GenericIdModel)
def get_course(data: GenericIdModel):
    return serialize_response(CourseGetModel, get_course_by_id(data.id))


@course_route.route("/", methods=['POST'])
@require_auth()
@validate_model_request(CourseCreateModel)
def post_course(data: CourseCreateModel):
    user_id = g.current_user.id
    posted = None if g.current_user.role == UserRole.user else datetime.utcnow()
    return serialize_response(CourseGetModel, create_course(data.title, data.text_content, posted, user_id,
                                                            data.category))


@course_route.route("/", methods=['PATCH'])
@require_auth()
@validate_model_params(CourseUpdateModel)
def update_course(data: CourseUpdateModel):
    course = get_course_by_id(data.id)
    owner_or_editor_check(course)
    args = data.dict()
    del args['id']
    update_course_by_id(data.id, **args)
    return "", HTTPStatus.OK


@course_route.route("/", methods=['DELETE'])
@require_auth()
@validate_model_params(GenericIdModel)
def delete_course(data: GenericIdModel):
    course = get_course_by_id(data.id)
    owner_or_editor_check(course)
    delete_course_by_id(data.id)
    return "", HTTPStatus.OK
