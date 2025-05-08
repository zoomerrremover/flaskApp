import datetime

from app.db.service.article_service import create_article, get_article_by_id, update_article_by_id, delete_article_by_id
from app.decorators import validate_model_request, validate_model_params, require_auth
from flask import Blueprint, render_template, Response, request, jsonify
from app.models.article import ArticleUpdate, ArticleCreate, ArticleDelete, ArticleSearch
from app.constants import UserRole
from datetime import datetime

article_route = Blueprint('article', __name__, url_prefix='/article')

@article_route.route("/", methods=['GET'])
@validate_model_params(ArticleSearch)
def get_article(data: ArticleSearch):
    return get_article_by_id(data.id)

@article_route.route("/", methods=['POST'])
@require_auth(UserRole.editor)
@validate_model_params(ArticleCreate)
def compose_article(data: ArticleCreate):
    user_id = request.current_user.id
    create_article(user_id, data.title, data.text_content, datetime.utcnow())

@article_route.route("/", methods=['PATCH'])
@require_auth(UserRole.editor)
@validate_model_params(ArticleUpdate)
def update_article(data: ArticleUpdate):
    return update_article_by_id(data.id, **data.dict())

@article_route.route("/", methods=['DELETE'])
@require_auth(UserRole.editor)
@validate_model_params(ArticleSearch)
def delete_article(data: ArticleSearch):
    return delete_article_by_id(data.id)
