from datetime import datetime, timezone
from http import HTTPStatus

from flask import Blueprint, g

from src.common import owner_or_editor_check, serialize_response
from src.constants import ErrorsMsgEnum
from src.db import Suggestion, SuggestionReaction
from src.decorators import (
    handle_db_exception,
    require_auth,
    validate_model_params,
    validate_model_request,
)
from src.exceptions import InvalidDataError
from src.models import (
    GenericIdModel,
    IdSearchModel,
    SuggestionCreateModel,
    SuggestionGetModel,
    SuggestionUpdateModel,
)

suggestion_route = Blueprint("suggestion_route", __name__, url_prefix="/suggestion")


@suggestion_route.route("/", methods=["GET"])
@validate_model_params(GenericIdModel)
def get_suggestion(data: GenericIdModel):
    return serialize_response(SuggestionGetModel, Suggestion.get_by_id(data.id))


@suggestion_route.route("/by_user", methods=["GET"])
@validate_model_params(IdSearchModel)
def get_suggestion_by_user(data: IdSearchModel):
    return serialize_response(
        SuggestionGetModel, Suggestion.get_by_user(data.id, data.limit)
    )


@suggestion_route.route("/by_article", methods=["GET"])
@validate_model_params(IdSearchModel)
def get_suggestion_by_article(data: IdSearchModel):
    return serialize_response(
        SuggestionGetModel, Suggestion.get_suggestion_by_article(data.id, data.limit)
    )


@suggestion_route.route("/", methods=["POST"])
@require_auth()
@validate_model_request(SuggestionCreateModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_SUGGESTION_UPDATE_FAILED)
def create_suggestion(data: SuggestionCreateModel):
    addon_data = {
        "user_id": g.current_user.id,
        "date_posted": datetime.now(timezone.utc),
    }
    return serialize_response(
        SuggestionGetModel, Suggestion.create(**data.model_dump(), **addon_data)
    )


@suggestion_route.route("/star", methods=["POST"])
@require_auth()
@validate_model_params(GenericIdModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_ALREDY_REACTED)
def star_suggestion(data: GenericIdModel):
    input_data = {"suggestion_id": data.id, "user_id": g.current_user.id}
    SuggestionReaction.create(**input_data)
    return " ", HTTPStatus.OK


@suggestion_route.route("/unstar", methods=["POST"])
@require_auth()
@validate_model_params(GenericIdModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_ALREDY_REACTED)
def unstar_suggestion(data: GenericIdModel):
    input_data = {"suggestion_id": data.id, "user_id": g.current_user.id}
    result = SuggestionReaction.delete_reaction(**input_data)
    if result == 0:
        raise InvalidDataError(ErrorsMsgEnum.ERROR_SUGGESTION_NOT_AFFECTED)
    return " ", HTTPStatus.OK


@suggestion_route.route("/", methods=["PATCH"])
@require_auth()
@validate_model_params(SuggestionUpdateModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_SUGGESTION_UPDATE_FAILED)
def update_suggestion(data: SuggestionUpdateModel):
    owner_or_editor_check(Suggestion.get_by_id(data.id))
    Suggestion.update_by_id(data.id, **data.model_dump(exclude={"id"}))
    return "", HTTPStatus.OK


@suggestion_route.route("/", methods=["DELETE"])
@require_auth()
@validate_model_params(GenericIdModel)
@handle_db_exception(ErrorsMsgEnum.ERROR_DELETE_FAILED)
def delete_suggestion(data: GenericIdModel):
    course = Suggestion.get_by_id(data.id)
    owner_or_editor_check(course)
    Suggestion.delete_by_id(data.id)
    return "", HTTPStatus.OK
