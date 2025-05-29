from app.models.suggestion import (
    SuggestionGetModel,
    SuggestionCreateModel,
    SuggestionUpdateModel,
    SuggestionReactionModel,
)
from app.db import Suggestion
from app.models.common import GenericIdModel
from app.decorators import (
    validate_model_params,
    validate_model_request,
    handle_exception,
)
from app.security.auth import require_auth
from app.common import serialize_response, owner_or_editor_check
from flask import Blueprint, render_template, Response, request, jsonify, g
from datetime import datetime
from http import HTTPStatus
from app.exceptions import InvalidDataError
from app.constants import ErrorsMsgEnum
from sqlalchemy.exc import IntegrityError

suggestion_route = Blueprint("suggestion_route", __name__, url_prefix="/suggestion")


@suggestion_route.route("/", methods=["GET"])
@validate_model_params(GenericIdModel)
def get_suggestion(data: GenericIdModel):
    return serialize_response(SuggestionGetModel, Suggestion.get_by_id(data.id))


@suggestion_route.route("/", methods=["POST"])
@require_auth()
@validate_model_request(SuggestionCreateModel)
@handle_exception(
    IntegrityError, InvalidDataError(ErrorsMsgEnum.ERR_SUGGESTION_UPDATE_CREATE)
)
def create_suggestion(data: SuggestionCreateModel):
    addon_data = {"user_id": g.current_user.id, "posted": datetime.utcnow()}
    return serialize_response(
        SuggestionGetModel, Suggestion.create(**data.dict(), **addon_data).save()
    )


@suggestion_route.route("/", methods=["PATCH"])
@require_auth()
@validate_model_params(SuggestionUpdateModel)
@handle_exception(
    IntegrityError, InvalidDataError(ErrorsMsgEnum.ERR_SUGGESTION_UPDATE_CREATE)
)
def update_suggestion(data: SuggestionUpdateModel):
    owner_or_editor_check(Suggestion.get_by_id(data.id))
    Suggestion.update(data.id, **data.dict(exclude={"id"}))
    return "", HTTPStatus.OK


@suggestion_route.route("/", methods=["DELETE"])
@require_auth()
@validate_model_params(GenericIdModel)
@handle_exception(IntegrityError, InvalidDataError(ErrorsMsgEnum.ERR_DELETE))
def delete_suggestion(data: GenericIdModel):
    course = Suggestion.get_by_id(data.id)
    owner_or_editor_check(course)
    Suggestion.delete(data.id)
    return "", HTTPStatus.OK
