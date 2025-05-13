import datetime
from http import HTTPStatus
from app.db.service.article_service import create_article, get_article_by_id, update_article_by_id, delete_article_by_id
from app.decorators import validate_model_request, validate_model_params, require_auth
from flask import Blueprint, render_template, Response, request, jsonify, g
from app.models.article import ArticleUpdate, ArticleCreate
from app.models.common import GenericIdModel
from app.constants import UserRole
from datetime import datetime

article_route = Blueprint('article', __name__, url_prefix='/article')

@article_route.route("/", methods=['GET'])
@validate_model_params(GenericIdModel)
def get_article(data: GenericIdModel):
    return get_article_by_id(data.id)

@article_route.route("/", methods=['POST'])
@require_auth(UserRole.editor)
@validate_model_params(ArticleCreate)
def compose_article(data: ArticleCreate):
    user_id = g.current_user.id
    create_article(user_id, data.title, data.text_content, datetime.utcnow())
    return HTTPStatus.OK

@article_route.route("/", methods=['PATCH'])
@require_auth(UserRole.editor)
@validate_model_params(ArticleUpdate)
def update_article(data: ArticleUpdate):
    update_article_by_id(data.id, **data.dict())
    return HTTPStatus.OK

@article_route.route("/", methods=['DELETE'])
@require_auth(UserRole.editor)
@validate_model_params(GenericIdModel)
def delete_article(data: GenericIdModel):
    delete_article_by_id(data.id)
    return HTTPStatus.OK
