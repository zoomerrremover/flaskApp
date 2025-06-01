# from flask import Blueprint, g
# from app.db.service.article import ArticleDbService
# from app.db.service.course import CourseDbService
# from app.db.service.suggestion import SuggestionDbService
# from app.db.service.user import UserDbService
# from app.models.common import StringSearchModel, GenericIdModel
# from app.decorators import validate_model_params
# from app.common import serialize_response
# from app.models.article import ArticleGetModel
# from app.models.course import CourseGetModel
# from app.models.suggestion import SuggestionGetModel
# from app.constants import UserRolesEnum
# from app.models.user import UserGetModel, UserAdminGetModel

# search_route = Blueprint('search_route', __name__, url_prefix='/search')


# @search_route.route("/article", methods=['GET'])
# @validate_model_params(StringSearchModel)
# def get_article_string(data: StringSearchModel):
#     return serialize_response(ArticleGetModel, ArticleDbService.search_by_query(data.search, data.limit))


# @search_route.route("/article_by_user", methods=['GET'])
# @validate_model_params(GenericIdModel)
# def get_article_by_user(data: GenericIdModel):
#     return serialize_response(ArticleGetModel, ArticleDbService.search_by_user(data.id, data.limit))


# @search_route.route("/article_by_course", methods=['GET'])
# @validate_model_params(GenericIdModel)
# def get_article_by_course(data: GenericIdModel):
#     return serialize_response(ArticleGetModel, ArticleDbService.search_by_course(data.id, data.limit))


# @search_route.route("/course", methods=['GET'])
# @validate_model_params(StringSearchModel)
# def get_course_string(data: StringSearchModel):
#     return serialize_response(CourseGetModel, CourseDbService.search_by_query(data.search, data.limit))


# @search_route.route("/course_by_user", methods=['GET'])
# @validate_model_params(GenericIdModel)
# def get_course_by_user(data: GenericIdModel):
#     return serialize_response(CourseGetModel, CourseDbService.search_by_user(data.id, data.limit))


# @search_route.route("/course_by_category", methods=['GET'])
# @validate_model_params(StringSearchModel)
# def get_course_by_category(data: StringSearchModel):
#     return serialize_response(CourseGetModel, CourseDbService.get_by_category(data.search, data.limit))


# @search_route.route("/suggestion", methods=['GET'])
# @validate_model_params(StringSearchModel)
# def get_suggestion_string(data: StringSearchModel):
#     return serialize_response(SuggestionGetModel, SuggestionDbService.search_by_query(data.search, data.limit))


# @search_route.route("/suggestion_by_user", methods=['GET'])
# @validate_model_params(GenericIdModel)
# def get_suggestion_by_user(data: GenericIdModel):
#     return serialize_response(SuggestionGetModel, SuggestionDbService.search_by_user(data.id, data.limit))


# @search_route.route("/suggestion_by_article", methods=['GET'])
# @validate_model_params(GenericIdModel)
# def get_suggestion_by_article(data: GenericIdModel):
#     return serialize_response(SuggestionGetModel, SuggestionDbService.search_by_article(data.id, data.limit))


# @search_route.route("/user", methods=['GET'])
# @validate_model_params(StringSearchModel)
# def get_user_string(data: StringSearchModel):
#     return serialize_response(
#         UserAdminGetModel if g.current_user.role == UserRolesEnum.admin else UserGetModel,
#         UserDbService.search_by_query(
#             data.search,
#             data.limit
#         )
#     )
