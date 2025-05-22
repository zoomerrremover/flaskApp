import datetime
from http import HTTPStatus
from app.db.service.article import ArticleDbService
from app.decorators import validate_model_request, validate_model_params, handle_exception
from app.security.auth import require_auth
from flask import Blueprint, render_template, Response, request, jsonify, g
from app.models.article import ArticleUpdateModel, ArticleCreateModel
from app.models.common import GenericIdModel
from app.constants import UserRolesEnum, ErrorsMsgEnum
from datetime import datetime
from app.common import serialize_response, owner_or_editor_check
from app.models.article import ArticleGetModel
from sqlalchemy.exc import IntegrityError
from app.exceptions import InvalidDataError

article_route = Blueprint('article', __name__, url_prefix='/article')


@article_route.route("/", methods=['GET'])
@validate_model_params(GenericIdModel)
def get_article(data: GenericIdModel):
    return serialize_response(ArticleGetModel, ArticleDbService.get_by_id(data.id))


@article_route.route("/", methods=['POST'])
@require_auth()
@validate_model_request(ArticleCreateModel)
@handle_exception(IntegrityError, InvalidDataError(ErrorsMsgEnum.ERR_ARTICLE_UPDATE_CREATE))
def post_article(data: ArticleCreateModel):
    addon_data = {
        "user_id": g.current_user.id,
        "date_created": datetime.utcnow(),
        "date_posted": None if g.current_user.role == UserRolesEnum.user else datetime.utcnow()
    }
    return serialize_response(ArticleGetModel, ArticleDbService.create(**data.dict(), **addon_data))


@article_route.route("/", methods=['PATCH'])
@require_auth(UserRolesEnum.editor)
@validate_model_params(ArticleUpdateModel)
@handle_exception(IntegrityError, InvalidDataError(ErrorsMsgEnum.ERR_ARTICLE_UPDATE_CREATE))
def update_article(data: ArticleUpdateModel):
    owner_or_editor_check(ArticleDbService.get_by_id(data.id))
    ArticleDbService.update(data.id, **data.dict(exclude={"id"}))
    return "", HTTPStatus.OK


@article_route.route("/", methods=['DELETE'])
@require_auth(UserRolesEnum.editor)
@validate_model_params(GenericIdModel)
@handle_exception(IntegrityError, InvalidDataError(ErrorsMsgEnum.ERR_DELETE))
def delete_article(data: GenericIdModel):
    owner_or_editor_check(ArticleDbService.get_by_id(data.id))
    ArticleDbService.delete(data.id)
    return "", HTTPStatus.OK
