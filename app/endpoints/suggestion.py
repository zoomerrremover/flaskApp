from app.models.suggestion import SuggestionGetModel, SuggestionCreateModel, SuggestionUpdateModel, \
                                   SuggestionReactionModel
from app.db.service.suggestion_service import \
    (
        create_suggestion,
        get_suggestion_by_id,
        get_suggestion_reaction,
        update_suggestion_by_id,
        update_reaction_to_suggestion,
        delete_suggestion_reaction,
        delete_suggestion_by_id
    )
from app.models.common import GenericIdModel
from app.decorators import require_auth, validate_model_params, validate_model_request
from app.common import serialize_response, owner_or_editor_check
from flask import Blueprint, render_template, Response, request, jsonify, g
from datetime import datetime
from http import HTTPStatus

suggestion_route = Blueprint('suggestion_route', __name__, url_prefix='/suggestion')


@suggestion_route.route("/", methods=['GET'])
@validate_model_params(GenericIdModel)
def get_suggestion(data: GenericIdModel):
    return serialize_response(SuggestionGetModel, get_suggestion_by_id(data.id))


@suggestion_route.route("/", methods=['POST'])
@require_auth()
@validate_model_request(SuggestionCreateModel)
def post_suggestion(data: SuggestionCreateModel):
    user_id = g.current_user.id
    posted = datetime.utcnow()
    return serialize_response(SuggestionGetModel, create_suggestion(data.title, data.text_content, posted, user_id,
                                                            data.article_id))


@suggestion_route.route("/", methods=['PATCH'])
@require_auth()
@validate_model_params(SuggestionUpdateModel)
def update_suggestion(data: SuggestionUpdateModel):
    course = get_suggestion_by_id(data.id)
    owner_or_editor_check(course)
    args = data.dict()
    del args['id']
    update_suggestion_by_id(data.id, **args)
    return "", HTTPStatus.OK


@suggestion_route.route("/", methods=['DELETE'])
@require_auth()
@validate_model_params(GenericIdModel)
def delete_suggestion(data: GenericIdModel):
    course = get_suggestion_by_id(data.id)
    owner_or_editor_check(course)
    delete_suggestion_by_id(data.id)
    return "", HTTPStatus.OK
