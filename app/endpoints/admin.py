from flask import Blueprint, render_template, Response, request, jsonify
from app.db.service.user_service import update_user_by_id, search_users_by_email, search_users_by_role
from app.decorators import require_auth, validate_model_request
from app.models.user import UserRoleUpdateModel, UserEmailModel, UserRoleModel

admin_route = Blueprint('admin_route', __name__, url_prefix='/admin')

@admin_route.route("/user/email_search", methods=['GET'])
@require_auth()
@validate_model_request(UserEmailModel)
def user_email_search(data: UserEmailModel):
    return search_users_by_email(data.email)


@admin_route.route("/user/role_search", methods=['GET'])
@require_auth()
@validate_model_request(UserRoleModel)
def user_role_search(data: UserRoleModel):
    return search_users_by_role(data.role)


@admin_route.route("/user_role", methods=['PATCH'])
@require_auth()
@validate_model_request(UserRoleUpdateModel)
def update_user_role(data: UserRoleUpdateModel):
    return update_user_by_id(data.id, **data.dict())
