import datetime
from http import HTTPStatus
from flask import Blueprint, render_template, Response, request, jsonify, g
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from ..db import Article
from ..decorators import (
    validate_model_request,
    validate_model_params,
    handle_db_exception,
    require_auth,
)
from ..models import (
    ArticleUpdateModel,
    ArticleCreateModel,
    GenericIdModel,
    ArticleGetModel,
)
from ..constants import UserRolesEnum, ErrorsMsgEnum
from ..common import serialize_response, owner_or_editor_check
from ..exceptions import InvalidDataError

article_route = Blueprint("article", __name__, url_prefix="/article")


@article_route.route("/", methods=["GET"])
@validate_model_params(GenericIdModel)
def get_article(data: GenericIdModel):
    return serialize_response(ArticleGetModel, Article.get_by_id(data.id))


@article_route.route("/", methods=["POST"])
@require_auth()
@validate_model_request(ArticleCreateModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_ARTICLE_UPDATE_CREATE)
def create_article(data: ArticleCreateModel):
    addon_data = {
        "user_id": g.current_user.id,
        "date_created": datetime.utcnow(),
        "date_posted": (
            None if g.current_user.role == UserRolesEnum.user else datetime.utcnow()
        ),
    }
    return serialize_response(
        ArticleGetModel, Article(**data.dict(), **addon_data).save()
    )


@article_route.route("/", methods=["PATCH"])
@require_auth(UserRolesEnum.editor)
@validate_model_params(ArticleUpdateModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_ARTICLE_UPDATE_CREATE)
def update_article(data: ArticleUpdateModel):
    owner_or_editor_check(Article.get_by_id(data.id))
    Article.update_by_id(data.id, **data.dict(exclude={"id"}))
    return "", HTTPStatus.OK


@article_route.route("/", methods=["DELETE"])
@require_auth(UserRolesEnum.editor)
@validate_model_params(GenericIdModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_DELETE)
def delete_article(data: GenericIdModel):
    owner_or_editor_check(Article.get_by_id(data.id))
    Article.delete_by_id(data.id)
    return "", HTTPStatus.OK
