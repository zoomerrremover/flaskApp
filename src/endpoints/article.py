from datetime import datetime, timezone
from http import HTTPStatus

from flask import Blueprint, g

from src.common import owner_or_editor_check, serialize_response
from src.constants import ErrorsMsgEnum, UserRolesEnum
from src.db import Article
from src.decorators import (
    handle_db_exception,
    require_auth,
    validate_model_params,
    validate_model_request,
)
from src.models import (
    ArticleCreateModel,
    ArticleGetModel,
    ArticleUpdateModel,
    GenericIdModel,
    IdSearchModel,
)

article_route = Blueprint("article", __name__, url_prefix="/article")


@article_route.route("/", methods=["GET"])
@validate_model_params(GenericIdModel)
def get_article(data: GenericIdModel):
    return serialize_response(ArticleGetModel, Article.get_by_id(data.id))


@article_route.route("/by_user", methods=["GET"])
@validate_model_params(IdSearchModel)
def get_article_by_user(data: IdSearchModel):
    return serialize_response(ArticleGetModel, Article.get_by_user(data.id, data.limit))


@article_route.route("/by_course", methods=["GET"])
@validate_model_params(IdSearchModel)
def get_article_by_course(data: IdSearchModel):
    return serialize_response(
        ArticleGetModel, Article.get_article_by_course(data.id, data.limit)
    )


@article_route.route("/", methods=["POST"])
@require_auth()
@validate_model_request(ArticleCreateModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_ARTICLE_UPDATE_FAILED)
def create_article(data: ArticleCreateModel):
    addon_data = {
        "user_id": g.current_user.id,
        "date_created": datetime.now(timezone.utc),
        "date_posted": None,
    }
    return serialize_response(
        ArticleGetModel, Article.create(**data.model_dump(), **addon_data)
    )


@article_route.route("post_article", methods=["PATCH"])
@require_auth(UserRolesEnum.EDITOR)
@validate_model_params(GenericIdModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_ARTICLE_UPDATE_FAILED)
def post_article(data: GenericIdModel):
    Article.update_by_id(data.id, **{"date_posted": datetime.now(timezone.utc)})
    return "", HTTPStatus.OK


@article_route.route("/", methods=["PATCH"])
@require_auth()
@validate_model_params(ArticleUpdateModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_ARTICLE_UPDATE_FAILED)
def update_article(data: ArticleUpdateModel):
    owner_or_editor_check(Article.get_by_id(data.id))
    Article.update_by_id(data.id, **data.model_dump(exclude={"id"}))
    return "", HTTPStatus.OK


@article_route.route("/", methods=["DELETE"])
@require_auth()
@validate_model_params(GenericIdModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_DELETE_FAILED)
def delete_article(data: GenericIdModel):
    owner_or_editor_check(Article.get_by_id(data.id))
    Article.delete_by_id(data.id)
    return "", HTTPStatus.OK
