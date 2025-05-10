from flask import Blueprint, render_template, Response, request, jsonify
from app.db.service.user_service import update_user_by_id
from app.decorators import require_auth, validate_model_request
from app.models.user import UserRoleUpdate

admin_route = Blueprint('admin_route', __name__, url_prefix='/admin')

@admin_route.route("/", methods=['PATCH'])
@require_auth()
@validate_model_request(UserRoleUpdate)
def update_user(data: UserRoleUpdate):
    return update_user_by_id(data.id, **data.dict())
