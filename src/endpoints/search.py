from flask import Blueprint

from src.common import serialize_response
from src.db import Article, Course, Suggestion, User
from src.decorators import validate_model_params
from src.models import (
    ArticleGetModel,
    ArticleSearchModel,
    CourseGetModel,
    StringSearchModel,
    SuggestionGetModel,
    SuggestionSearchModel,
    UserGetModel,
)

search_route = Blueprint("search_route", __name__, url_prefix="/search")


@search_route.route("/article", methods=["GET"])
@validate_model_params(ArticleSearchModel)
def get_article_string(data: ArticleSearchModel):
    return serialize_response(
        ArticleGetModel,
        Article.search(data.course_id, data.search_query, data.limit),
    )


@search_route.route("/course", methods=["GET"])
@validate_model_params(StringSearchModel)
def get_course_string(data: StringSearchModel):
    return serialize_response(
        CourseGetModel, Course.search(data.search_query, data.limit)
    )


@search_route.route("/suggestion", methods=["GET"])
@validate_model_params(SuggestionSearchModel)
def get_suggestion_string(data: SuggestionSearchModel):
    return serialize_response(
        SuggestionGetModel,
        Suggestion.search(data.search_query, data.article_id, data.limit),
    )


@search_route.route("/user", methods=["GET"])
@validate_model_params(StringSearchModel)
def get_user_string(data: StringSearchModel):
    return serialize_response(
        UserGetModel,
        User.search(data.search_query, data.limit),
    )
