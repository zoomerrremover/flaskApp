import datetime
from http import HTTPStatus
from app.db.service.article import create_article, get_article_by_id, update_article_by_id, delete_article_by_id
from app.decorators import validate_model_request, validate_model_params
from app.security.auth import require_auth
from flask import Blueprint, render_template, Response, request, jsonify, g
from app.models.article import ArticleUpdateModel, ArticleCreateModel
from app.models.common import GenericIdModel
from app.constants import UserRolesEnum
from datetime import datetime
from app.common import serialize_response, owner_or_editor_check
from app.models.article import ArticleGetModel

article_route = Blueprint('article', __name__, url_prefix='/article')


@article_route.route("/", methods=['GET'])
@validate_model_params(GenericIdModel)
def get_article(data: GenericIdModel):
    return serialize_response(ArticleGetModel, get_article_by_id(data.id))


@article_route.route("/", methods=['POST'])
@require_auth()
@validate_model_request(ArticleCreateModel)
def post_article(data: ArticleCreateModel):
    user_id = g.current_user.id
    posted = None if g.current_user.role == UserRolesEnum.user else datetime.utcnow()
    return (
        serialize_response(
            ArticleGetModel,
            create_article(
                data.title,
                data.text_content,
                user_id,
                data.course_id,
                posted,
                data.next_article,
                data.previous_article
            )
        )
    )


@article_route.route("/", methods=['PATCH'])
@require_auth(UserRolesEnum.editor)
@validate_model_params(ArticleUpdateModel)
def update_article(data: ArticleUpdateModel):
    owner_or_editor_check(get_article_by_id(data.id))
    update_article_by_id(data.id, **data.dict(exclude={"id"}))
    return "", HTTPStatus.OK


@article_route.route("/", methods=['DELETE'])
@require_auth(UserRolesEnum.editor)
@validate_model_params(GenericIdModel)
def delete_article(data: GenericIdModel):
    owner_or_editor_check(get_article_by_id(data.id))
    delete_article_by_id(data.id)
    return "", HTTPStatus.OK
